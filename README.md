# 三种命理系统排盘工具 triple_chart_parser.py

## 简介

本工具支持三种命理系统的结构化排盘：
- **八字（四柱）**：使用 `sxtwl` 库，支持真太阳时计算，输出四柱、五行分布、身强身弱分析
- **紫微斗数**：使用 `py-iztro` 库，输出命宫、身宫、主星位置、四化飞星
- **印度星盘**：使用 `flatlib` 库，设置恒星系统，输出上升星座、行星位置

## 安装依赖

建议使用 Python 虚拟环境：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
.\venv\Scripts\Activate.ps1
# Mac/Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

## 使用方法

### 基本使用（输出到控制台）
```bash
python triple_chart_parser.py --birth-date 2000-08-16 --birth-time 10:00 --timezone +8 --longitude 116.4 --latitude 39.9 --gender 1
```

### 保存为JSON文件（推荐）
```bash
python triple_chart_parser.py --birth-date 2000-08-16 --birth-time 10:00 --timezone +8 --longitude 116.4 --latitude 39.9 --gender 1 --save-file --location 北京
```

### 参数说明
- `--birth-date`：出生日期，格式：YYYY-MM-DD（如：2000-08-16）
- `--birth-time`：出生时间，格式：HH:MM（如：10:00）
- `--timezone`：时区，格式：+8或-5
- `--longitude`：经度（浮点数，如：116.4）
- `--latitude`：纬度（浮点数，如：39.9）
- `--gender`：性别，1=男，0=女
- `--save-file`：可选，保存为JSON文件而不是输出到控制台
- `--location`：可选，出生地点名称（用于文件命名）

### 常用示例

```bash
# 男性，北京出生
python triple_chart_parser.py --birth-date 1990-05-20 --birth-time 14:30 --timezone +8 --longitude 116.4 --latitude 39.9 --gender 1 --save-file --location 北京

# 女性，上海出生
python triple_chart_parser.py --birth-date 1995-10-15 --birth-time 08:45 --timezone +8 --longitude 121.5 --latitude 31.2 --gender 0 --save-file --location 上海

# 海外出生（纽约时区）
python triple_chart_parser.py --birth-date 1988-12-25 --birth-time 18:20 --timezone -5 --longitude -74.0 --latitude 40.7 --gender 1 --save-file --location 纽约
```

## 输出文件命名规则

当使用 `--save-file` 参数时，文件名格式为：
```
{性别}_{出生日期}_{出生时间}_{地点}_{经度}_{纬度}.json
```
例如：`1_20000816_1000_北京_116.4_39.9.json`

## 输出结果结构

```json
{
  "input": {
    "birth_date": "出生日期",
    "birth_time": "出生时间", 
    "timezone": "时区",
    "longitude": "经度",
    "latitude": "纬度",
    "gender": "性别数值",
    "gender_str": "性别文字"
  },
  "bazi": {
    "四柱信息": "...",
    "五行分析": "...",
    "身强身弱": "..."
  },
  "ziwei": {
    "命宫信息": "...",
    "十二宫星耀": "...",
    "四化分析": "..."
  },
  "vedic": {
    "上升星座": "...",
    "行星位置": "...",
    "宫位分布": "..."
  }
}
```

## 故障排查

- **缺少依赖库**：运行 `pip install -r requirements.txt`
- **时间计算异常**：检查时区格式是否正确（使用数字格式，如+8、-5）
- **经纬度输入异常**：确保使用浮点数格式
- **环境问题**：确保已激活Python虚拟环境

## 技术说明

- **八字系统**：基于寿星万年历库，支持真太阳时校正
- **紫微斗数**：基于传统排盘算法，支持现代简化输出
- **印度星盘**：基于西方占星学库，使用热带黄道系统

## 许可证

本项目仅供学习和研究使用。 