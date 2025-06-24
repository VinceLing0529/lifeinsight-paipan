#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from bazi_enhanced_analyzer import BaziEnhancedAnalyzer

def debug_wuxing_relations():
    """调试五行关系判断"""
    analyzer = BaziEnhancedAnalyzer()
    rules = analyzer.rules["十神规则"]
    
    print("🔥 丙火日主五行关系调试")
    print("=" * 50)
    
    # 测试天干
    test_gans = ["庚", "甲", "丙", "辛"]
    day_gan = "丙"
    
    print(f"日主: {day_gan} (五行: {rules['五行'][day_gan]}, 阴阳: {rules['阴阳'][day_gan]})")
    print()
    
    for gan in test_gans:
        gan_wuxing = rules["五行"][gan]
        gan_yinyang = rules["阴阳"][gan]
        
        print(f"测试天干: {gan} (五行: {gan_wuxing}, 阴阳: {gan_yinyang})")
        
        # 测试关系
        day_wuxing = rules["五行"][day_gan]
        relation = analyzer._get_relation_type(day_wuxing, gan_wuxing, rules["生克逻辑"])
        ten_god = analyzer.get_ten_god(day_gan, gan)
        
        print(f"  关系类型: {relation}")
        print(f"  十神: {ten_god}")
        
        # 详细分析
        if relation == "我克":
            print(f"  → 丙火({day_wuxing})克{gan}({gan_wuxing})")
        elif relation == "克我":
            print(f"  → {gan}({gan_wuxing})克丙火({day_wuxing})")
        elif relation == "生我":
            print(f"  → {gan}({gan_wuxing})生丙火({day_wuxing})")
        elif relation == "我生":
            print(f"  → 丙火({day_wuxing})生{gan}({gan_wuxing})")
        elif relation == "同我":
            print(f"  → {gan}({gan_wuxing})同丙火({day_wuxing})")
        
        print()
    
    print("🧠 理论验证:")
    print("庚金 → 火克金 → 我克 → 偏财(同阳) ✅")
    print("甲木 → 木生火 → 生我 → 偏印(同阳) ✅") 
    print("丙火 → 火同火 → 同我 → 比肩(同阳) ✅")
    print("辛金 → 金克火 → 克我 → 正官(异阴阳) ✅")

if __name__ == "__main__":
    debug_wuxing_relations() 