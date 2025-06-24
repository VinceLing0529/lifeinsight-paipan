#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

def check_logic():
    with open('bazi_rule_tables.json', 'r', encoding='utf-8') as f:
        rules = json.load(f)
    
    wo_ke_logic = rules['十神规则']['生克逻辑']['我克']
    ke_wo_logic = rules['十神规则']['生克逻辑']['克我']
    
    print("我克规则:")
    for k, v in wo_ke_logic.items():
        print(f"{k} 克 {v}")
    
    print(f"\n克我规则:")
    for k, v in ke_wo_logic.items():
        print(f"{k} 被 {v} 克")
    
    print(f"\n火被什么克: {ke_wo_logic.get('火')}")
    print(f"金被什么克: {ke_wo_logic.get('金')}")
    
    print(f"\n对于丙火日主和辛金:")
    print(f"火克金?: {wo_ke_logic.get('火') == '金'}")
    print(f"金克火?: {ke_wo_logic.get('火') == '金'}")

if __name__ == "__main__":
    check_logic() 