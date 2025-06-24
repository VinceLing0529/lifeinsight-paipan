#!/usr/bin/env python3
"""
紫微斗数高级API功能演示脚本
"""

from ziwei_advanced_api import ZiweiAdvancedAPI
import json

def test_all_features():
    """测试所有紫微斗数高级功能"""
    
    # 初始化API
    print("=== 初始化紫微斗数API ===")
    api = ZiweiAdvancedAPI("1998-05-29", 4, "男")
    print("✅ API初始化成功")
    print()
    
    # A类：基础信息
    print("=== A类：基础信息 ===")
    
    # A1. 获取星盘图
    print("A1. 获取星盘图：")
    chart = api.get_ziwei_chart()
    print(f"十四主星落宫：{chart['star_positions']}")
    print()
    
    # A2. 获取四柱
    print("A2. 获取四柱：")
    pillars = api.get_four_pillars()
    print(f"四柱：{pillars}")
    print()
    
    # A3. 年干四化
    print("A3. 年干四化：")
    trans = api.year_four_trans()
    print(f"年干四化：{trans}")
    print()
    
    # A4. 查询星耀位置
    print("A4. 查询星耀位置：")
    stars_to_check = ["紫微", "天机", "太阳", "武曲"]
    for star in stars_to_check:
        position = api.star_position(star)
        print(f"{star} → {position}")
    print()
    
    # A5. 判断空宫
    print("A5. 判断空宫：")
    houses_to_check = ["命宫", "疾厄", "迁移"]
    for house in houses_to_check:
        is_empty = api.is_empty_house(house)
        print(f"{house} → {'空宫' if is_empty else '有星'}")
    print()
    
    # B类：运势核心
    print("=== B类：运势核心 ===")
    
    # B1. 大限宫位
    print("B1. 大限宫位：")
    ages = [15, 25, 35, 45]
    for age in ages:
        fortune = api.major_fortune(age)
        print(f"{age}岁大限 → {fortune}")
    print()
    
    # B3. 流年分析
    print("B3. 流年分析：")
    years = [2020, 2024, 2025]
    for year in years:
        flow = api.flow_year(year)
        print(f"{year}年流年 → {flow}")
    print()
    
    # B4. 流年四化
    print("B4. 流年四化：")
    for year in years:
        flow_trans = api.flow_trans(year)
        print(f"{year}年四化 → {flow_trans}")
    print()
    
    # B5. 流年宫位
    print("B5. 流年宫位：")
    for year in years:
        house = api.house_of_flow(year)
        print(f"{year}年 → {house}")
    print()
    
    # C类：三方四正逻辑
    print("=== C类：三方四正逻辑 ===")
    
    # C1. 三方四正宫位
    print("C1. 三方四正宫位：")
    main_houses = ["命宫", "财帛", "官禄"]
    for house in main_houses:
        tri_houses = api.tri_house(house)
        print(f"{house}三方四正 → {tri_houses}")
    print()
    
    # C2. 三方四正含星判断
    print("C2. 三方四正含星判断：")
    test_cases = [
        ("命宫", "紫微"),
        ("财帛", "武曲"),
        ("官禄", ["天梁", "文昌"])
    ]
    for house, stars in test_cases:
        has_star = api.tri_has_star(house, stars)
        print(f"{house}三方四正含{stars} → {has_star}")
    print()
    
    # C3. 三方四正含四化判断
    print("C3. 三方四正含四化判断：")
    trans_types = ["禄", "权", "科", "忌"]
    for trans_type in trans_types:
        has_trans = api.tri_has_trans("命宫", trans_type)
        print(f"命宫三方四正含{trans_type} → {has_trans}")
    print()
    
    # C4. 星耀三方四正
    print("C4. 星耀三方四正：")
    major_stars = ["紫微", "天机", "武曲"]
    for star in major_stars:
        tri_houses = api.star_tri_house(star)
        print(f"{star}三方四正 → {tri_houses}")
    print()
    
    print("=== 所有功能测试完成 ===")

if __name__ == "__main__":
    test_all_features() 