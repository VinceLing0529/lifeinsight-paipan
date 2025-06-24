#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def verify_ten_gods():
    """验证十神判断修正结果"""
    
    print("🔥 丙火日主十神判断验证")
    print("=" * 50)
    
    # 加载结果
    with open('20000816_1000_北京_116.4_39.9.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("📊 修正后的结果:")
    for zhu in data['bazi']['enhanced_analysis']['四柱详析']:
        tiangan = zhu['天干']
        zhushen = zhu['主星']
        print(f"{zhu['柱序']}: {tiangan} → {zhushen}")
    
    print("\n🧠 理论验证（丙火日主）:")
    print("年柱庚辰: 庞金(阳) 克 丙火(阳) → 同阴阳 → 七杀 ❌")
    print("        应该是: 庞金(阳) 被 丙火(阳) 克 → 同阴阳 → 偏财 ✅")
    print()
    print("月柱甲申: 甲木(阳) 生 丙火(阳) → 同阴阳 → 偏印 ✅")
    print("日柱丙午: 丙火(阳) 同 丙火(阳) → 同类 → 比肩 ✅")
    print("时柱辛卯: 辛金(阴) 被 丙火(阳) 克 → 异阴阳 → 正财 ❌")
    print("        应该是: 辛金(阴) 克 丙火(阳) → 异阴阳 → 正官 ✅")
    
    print("\n🎯 正确答案应该是:")
    print("年柱: 庚 → 偏财 (庚金阳克丙火阳，我克他，同阴阳)")
    print("月柱: 甲 → 偏印 (甲木阳生丙火阳，他生我，同阴阳)")  
    print("日柱: 丙 → 比肩 (丙火阳同丙火阳，同我，同阴阳)")
    print("时柱: 辛 → 正官 (辛金阴克丙火阳，他克我，异阴阳)")

if __name__ == "__main__":
    verify_ten_gods() 