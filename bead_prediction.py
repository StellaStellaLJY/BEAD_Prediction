# -*- coding: utf-8 -*-
import pandas as pd
import urllib.request
import sys
import json
import joblib
from xgboost import Booster
import xgboost as xgb


def fetch_weather_data():
    try:
        # 请求天气数据
        ResultBytes = urllib.request.urlopen(
            "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/chicago/next24hours?unitGroup=us&elements=datetime%2Ctemp%2Cprecip%2Cpreciptype%2Cwindspeed%2Cuvindex%2Cicon&include=hours%2Ccurrent&key=AAKHVD69CLXCJ4UNBZ69L9RPM&contentType=json"
        )

        # 解析 JSON 数据
        jsonData = json.load(ResultBytes)
        return jsonData

    except urllib.error.HTTPError as e:
        ErrorInfo = e.read().decode()
        raise Exception(f'HTTPError: {e.code}, {ErrorInfo}')
    except urllib.error.URLError as e:
        raise Exception(f'URLError: {str(e)}')


def prepare_data(jsonData):
    # 提取小时数据
    hourly_data = jsonData["days"][0]["hours"]
    date_str = jsonData["days"][0]["datetime"]  # 日期，例如 '2025-04-22'

    # 转换为 DataFrame
    df = pd.DataFrame(hourly_data)

    # 处理数据
    df["preciptype"] = df["preciptype"].apply(lambda x: x[0] if isinstance(x, list) else x)
    df["timestamp"] = pd.to_datetime(date_str + " " + df["datetime"])

    # 时间衍生变量
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["hour"] = df["timestamp"].dt.hour
    df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)
    df["year_month"] = df["timestamp"].dt.to_period("M").astype(str)
    df["time_index"] = (df["timestamp"] - pd.Timestamp("2000-01-01")).dt.days

    # 创建 precip_rain / precip_snow 特征
    df["precip_rain"] = df["preciptype"].apply(lambda x: 1 if x == "rain" else 0)
    df["precip_snow"] = df["preciptype"].apply(lambda x: 1 if x == "snow" else 0)

    # 选择需要的列
    final_df = df[[ 
        "timestamp", 
        "temp", "precip", "windspeed", "uvindex", "icon",
        "year", "month", "day_of_week", "hour", "is_weekend",
        "year_month", "time_index", "precip_rain", "precip_snow"
    ]]


    return final_df

def process_and_predict():

    model = Booster()
    model.load_model("xgb_model_CV_3.0.json")
    
    # 读取站点映射
    station_mapping = pd.read_csv("station_mapping.csv")

    # 获取天气数据
    jsonData = fetch_weather_data()

    # 处理数据
    df = prepare_data(jsonData)

    # 执行笛卡尔积
    df['key'] = 1
    station_mapping['key'] = 1
    X = pd.merge(df, station_mapping, on='key')
    X = X.drop(columns=['key'])

    # 编码类别变量
    categorical_cols = ["icon"]
    X[categorical_cols] = X[categorical_cols].astype("category")
    X[categorical_cols] = X[categorical_cols].apply(lambda x: x.cat.codes)

    # 选择最终列
    desired_cols = [
        'timestamp', 'lat', 'lng', 'temp', 'precip',
        'windspeed', 'uvindex', 'icon', 'year', 'month', 'day_of_week',
        'hour', 'is_weekend', 'year_month', 'time_index',
        'precip_rain', 'precip_snow'
    ]
    X = X[desired_cols]

    # 删除时间戳列并确保是数值数据
    timestamps = X['timestamp']
    X_no_timestamp = X.drop(columns=['timestamp'])
    X_no_timestamp = X_no_timestamp.select_dtypes(include=["number"])
    
    # ✅ 转成DMatrix
    dmatrix_data = xgb.DMatrix(X_no_timestamp)
    
    # 模型预测
    X['predicted_inventory_change'] = model.predict(dmatrix_data).round().astype(int)
    
    # 还原时间戳
    X['timestamp'] = timestamps


    # 返回最终结果
    result = X[[
        'timestamp', 'lat', 'lng', 'temp', 'precip',
        'windspeed', 'uvindex', 'icon', 'year', 'month', 'day_of_week',
        'hour', 'is_weekend', 'year_month', 'time_index',
        'precip_rain', 'precip_snow', 'predicted_inventory_change'
    ]]

    return result

