#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
命理图表可视化工具
支持八字排盘图、紫微斗数命盘图、印度星盘图的生成
"""

import json
import argparse
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Rectangle, Polygon
import numpy as np
from pathlib import Path
import sys

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ChartVisualizer:
    def __init__(self, json_file):
        """初始化图表可视化器"""
        self.json_file = json_file
        self.data = self.load_data()
        
    def load_data(self):
        """加载JSON数据"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ 加载JSON文件失败: {e}")
            sys.exit(1)
    
    def generate_bazi_chart(self, save_path=None):
        """生成八字排盘图"""
        print("🎨 生成八字排盘图...")
        
        fig, ax = plt.subplots(1, 1, figsize=(16, 10))
        ax.set_xlim(0, 16)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        # 标题
        birth_info = self.data['input']
        title = f"八字排盘图 - {birth_info['birth_date']} {birth_info['birth_time']} {birth_info.get('location', '')}"
        ax.text(8, 9.5, title, ha='center', va='center', fontsize=18, fontweight='bold')
        
        # 四柱数据
        bazi_data = self.data['bazi']
        enhanced = bazi_data.get('enhanced_analysis', {})
        pillars = enhanced.get('四柱详析', [])
        
        # 柱名
        pillar_names = ['年柱', '月柱', '日柱', '时柱']
        pillar_positions = [2, 5, 8, 11]
        
        # 绘制四柱
        for i, (name, pos) in enumerate(zip(pillar_names, pillar_positions)):
            if i < len(pillars):
                pillar = pillars[i]
                
                # 柱名
                ax.text(pos, 8.5, name, ha='center', va='center', fontsize=14, fontweight='bold')
                
                # 天干
                tiangan = pillar['天干']
                color = 'red' if name == '日柱' else 'black'  # 日主高亮
                ax.add_patch(Rectangle((pos-0.8, 7), 1.6, 0.8, facecolor='lightblue', edgecolor='black'))
                ax.text(pos, 7.4, tiangan, ha='center', va='center', fontsize=16, fontweight='bold', color=color)
                
                # 地支
                dizhi = pillar['地支']
                ax.add_patch(Rectangle((pos-0.8, 6), 1.6, 0.8, facecolor='lightgreen', edgecolor='black'))
                ax.text(pos, 6.4, dizhi, ha='center', va='center', fontsize=16, fontweight='bold')
                
                # 主星（十神）
                zhuxing = pillar.get('主星', '')
                ax.add_patch(Rectangle((pos-0.8, 5), 1.6, 0.8, facecolor='lightyellow', edgecolor='black'))
                ax.text(pos, 5.4, zhuxing, ha='center', va='center', fontsize=12, fontweight='bold')
                
                # 藏干
                canggan = pillar.get('藏干', [])
                if canggan:
                    canggan_text = ' '.join(canggan)
                    ax.add_patch(Rectangle((pos-0.8, 4), 1.6, 0.8, facecolor='lightcyan', edgecolor='black'))
                    ax.text(pos, 4.4, canggan_text, ha='center', va='center', fontsize=10)
                
                # 纳音
                nayin = pillar.get('纳音', '')
                if nayin:
                    ax.text(pos, 3.5, nayin, ha='center', va='center', fontsize=10, style='italic')
        
        # 图例
        legend_y = 2.5
        ax.text(1, legend_y, '图例:', fontsize=12, fontweight='bold')
        
        # 颜色图例
        legend_items = [
            ('天干', 'lightblue'),
            ('地支', 'lightgreen'), 
            ('十神', 'lightyellow'),
            ('藏干', 'lightcyan')
        ]
        
        for i, (label, color) in enumerate(legend_items):
            x_pos = 2.5 + i * 2.5
            ax.add_patch(Rectangle((x_pos-0.3, legend_y-0.2), 0.6, 0.4, facecolor=color, edgecolor='black'))
            ax.text(x_pos+0.8, legend_y, label, ha='left', va='center', fontsize=10)
        
        # 五行统计
        wuxing_count = bazi_data.get('five_elements_count', {})
        if wuxing_count:
            ax.text(1, 1.5, '五行统计:', fontsize=12, fontweight='bold')
            wuxing_text = ' '.join([f"{k}:{v}" for k, v in wuxing_count.items()])
            ax.text(1, 1, wuxing_text, fontsize=11)
        
        # 身强身弱
        body_strength = bazi_data.get('body_strength', '')
        if body_strength:
            ax.text(1, 0.5, f'身强身弱: {body_strength}', fontsize=12, fontweight='bold', 
                   color='red' if body_strength == '强' else 'blue')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ 八字排盘图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_ziwei_chart(self, save_path=None):
        """生成紫微斗数命盘图"""
        print("🎨 生成紫微斗数命盘图...")
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.axis('off')
        ax.set_aspect('equal')
        
        # 标题
        birth_info = self.data['input']
        title = f"紫微斗数命盘 - {birth_info['birth_date']} {birth_info['birth_time']}"
        ax.text(0, 5.5, title, ha='center', va='center', fontsize=16, fontweight='bold')
        
        # 12宫位置（从命宫开始，逆时针）
        palace_positions = [
            (2, 2), (2, 0), (2, -2), (0, -2),    # 命宫、父母、福德、田宅
            (-2, -2), (-2, 0), (-2, 2), (0, 2),  # 官禄、交友、迁移、疾厄
            (4, 2), (4, 0), (4, -2), (0, 4)      # 财帛、子女、夫妻、兄弟
        ]
        
        # 宫位名称
        palace_names = [
            '命宫', '父母', '福德', '田宅',
            '官禄', '交友', '迁移', '疾厄', 
            '财帛', '子女', '夫妻', '兄弟'
        ]
        
        # 绘制宫位格子
        ziwei_data = self.data.get('ziwei', {})
        chart_data = ziwei_data.get('chart', {})
        palaces_data = chart_data.get('palaces', {})
        
        for i, (pos, name) in enumerate(zip(palace_positions, palace_names)):
            x, y = pos
            
            # 绘制宫位方框
            rect = Rectangle((x-0.9, y-0.9), 1.8, 1.8, facecolor='lightblue', 
                           edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            
            # 宫位名称
            ax.text(x, y+0.7, name, ha='center', va='center', fontsize=10, fontweight='bold')
            
            # 查找对应宫位数据
            palace_data = None
            for palace_name, data in palaces_data.items():
                if palace_name in name or name in palace_name:
                    palace_data = data
                    break
            
            if palace_data:
                # 主星
                major_stars = palace_data.get('major_stars', [])
                if major_stars:
                    star_names = []
                    for star in major_stars:
                        star_name = star.get('name', '') if isinstance(star, dict) else str(star)
                        brightness = star.get('brightness', '') if isinstance(star, dict) else ''
                        if brightness and brightness != '':
                            star_names.append(f"{star_name}({brightness})")
                        else:
                            star_names.append(star_name)
                    
                    star_text = '\n'.join(star_names[:2])  # 最多显示2个主星
                    ax.text(x, y+0.2, star_text, ha='center', va='center', fontsize=8, 
                           fontweight='bold', color='red')
                
                # 副星
                minor_stars = palace_data.get('minor_stars', [])
                if minor_stars:
                    minor_text = ' '.join(minor_stars[:3])  # 最多显示3个副星
                    ax.text(x, y-0.2, minor_text, ha='center', va='center', fontsize=7, color='blue')
                
                # 身宫标记
                if palace_data.get('is_body_palace', False):
                    ax.text(x+0.6, y+0.6, '身', ha='center', va='center', fontsize=8, 
                           fontweight='bold', color='green',
                           bbox=dict(boxstyle="circle,pad=0.1", facecolor='yellow'))
        
        # 中央信息
        basic_info = ziwei_data.get('basic_info', {})
        center_text = []
        if basic_info.get('soul'):
            center_text.append(f"命: {basic_info['soul']}")
        if basic_info.get('body'):
            center_text.append(f"身: {basic_info['body']}")
        if basic_info.get('five_elements_class'):
            center_text.append(basic_info['five_elements_class'])
        
        if center_text:
            ax.text(0, 0, '\n'.join(center_text), ha='center', va='center', 
                   fontsize=12, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.3", facecolor='lightyellow'))
        
        # 农历日期
        lunar_date = basic_info.get('lunar_date', '')
        if lunar_date:
            ax.text(0, -5.5, f"农历: {lunar_date}", ha='center', va='center', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ 紫微斗数命盘图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_vedic_chart(self, save_path=None):
        """生成印度星盘图（南印度样式）"""
        print("🎨 生成印度星盘图...")
        
        fig, ax = plt.subplots(1, 1, figsize=(12, 12))
        ax.set_xlim(-6, 6)
        ax.set_ylim(-6, 6)
        ax.axis('off')
        ax.set_aspect('equal')
        
        # 标题
        birth_info = self.data['input']
        title = f"印度星盘 (Vedic Chart) - {birth_info['birth_date']} {birth_info['birth_time']}"
        ax.text(0, 5.5, title, ha='center', va='center', fontsize=16, fontweight='bold')
        
        # 南印度样式：菱形12宫布局
        # 绘制外框
        outer_square = Rectangle((-4, -4), 8, 8, facecolor='none', edgecolor='black', linewidth=3)
        ax.add_patch(outer_square)
        
        # 绘制内部分割线
        # 水平线
        ax.plot([-4, 4], [1.33, 1.33], 'k-', linewidth=2)
        ax.plot([-4, 4], [-1.33, -1.33], 'k-', linewidth=2)
        # 垂直线
        ax.plot([-1.33, -1.33], [-4, 4], 'k-', linewidth=2)
        ax.plot([1.33, 1.33], [-4, 4], 'k-', linewidth=2)
        
        # 对角线
        ax.plot([-4, -1.33], [4, 1.33], 'k-', linewidth=2)
        ax.plot([1.33, 4], [4, 1.33], 'k-', linewidth=2)
        ax.plot([-4, -1.33], [-4, -1.33], 'k-', linewidth=2)
        ax.plot([1.33, 4], [-4, -1.33], 'k-', linewidth=2)
        
        # 重新定义12宫位置（避免重叠）
        house_positions = {
            1: (0, 2.67),       # 第1宫（上中）
            2: (-2.67, 2.67),   # 第2宫（左上角）
            3: (-2.67, 0),      # 第3宫（左中）
            4: (-2.67, -2.67),  # 第4宫（左下角）
            5: (0, -2.67),      # 第5宫（下中）
            6: (2.67, -2.67),   # 第6宫（右下角）
            7: (2.67, 0),       # 第7宫（右中）
            8: (2.67, 2.67),    # 第8宫（右上角）
            9: (0, 0.67),       # 第9宫（中上）
            10: (-0.67, 0),     # 第10宫（中左）
            11: (0, -0.67),     # 第11宫（中下）
            12: (0.67, 0)       # 第12宫（中右）
        }
        
        # 宫位名称
        house_names = {
            1: "1st\n(Asc)", 2: "2nd", 3: "3rd", 4: "4th",
            5: "5th", 6: "6th", 7: "7th", 8: "8th",
            9: "9th", 10: "10th", 11: "11th", 12: "12th"
        }
        
        # 获取印度星盘数据
        vedic_data = self.data.get('vedic', {})
        planets_data = vedic_data.get('planets', {})
        houses_data = vedic_data.get('houses', {})
        
        # 为每个宫位收集行星信息
        house_planets = {i: [] for i in range(1, 13)}
        
        # 分析行星在各宫位的分布
        for planet_name, planet_info in planets_data.items():
            if isinstance(planet_info, dict):
                house_num = planet_info.get('house')
                if house_num and 1 <= house_num <= 12:
                    # 简化行星名称
                    planet_abbr = {
                        'Sun': 'Su', 'Moon': 'Mo', 'Mercury': 'Me', 'Venus': 'Ve',
                        'Mars': 'Ma', 'Jupiter': 'Ju', 'Saturn': 'Sa', 
                        'Rahu': 'Ra', 'Ketu': 'Ke', 'Uranus': 'Ur', 
                        'Neptune': 'Ne', 'Pluto': 'Pl'
                    }.get(planet_name, planet_name[:2])
                    
                    sign = planet_info.get('sign', '')
                    sign_abbr = sign[:3] if sign else ''
                    house_planets[house_num].append(f"{planet_abbr}\n{sign_abbr}")
        
        # 绘制各宫位信息
        for house_num in range(1, 13):
            x, y = house_positions[house_num]
            
            # 宫位名称（较小字体，放在角落）
            name_offset_x = -0.8 if x < 0 else (0.8 if x > 0 else 0)
            name_offset_y = 0.8 if y > 0 else (-0.8 if y < 0 else 0.8)
            
            ax.text(x + name_offset_x, y + name_offset_y, house_names[house_num], 
                   ha='center', va='center', fontsize=8, fontweight='bold',
                   bbox=dict(boxstyle="round,pad=0.2", facecolor='lightblue', alpha=0.7))
            
            # 显示该宫位的行星
            planets_in_house = house_planets[house_num]
            if planets_in_house:
                # 限制显示的行星数量，避免重叠
                display_planets = planets_in_house[:3]  # 最多显示3个行星
                
                if len(display_planets) == 1:
                    # 单个行星居中显示
                    ax.text(x, y, display_planets[0], ha='center', va='center', 
                           fontsize=9, fontweight='bold', color='red')
                elif len(display_planets) == 2:
                    # 两个行星上下排列
                    ax.text(x, y + 0.2, display_planets[0], ha='center', va='center', 
                           fontsize=8, fontweight='bold', color='red')
                    ax.text(x, y - 0.2, display_planets[1], ha='center', va='center', 
                           fontsize=8, fontweight='bold', color='red')
                else:
                    # 三个行星紧凑排列
                    ax.text(x, y + 0.3, display_planets[0], ha='center', va='center', 
                           fontsize=7, fontweight='bold', color='red')
                    ax.text(x, y, display_planets[1], ha='center', va='center', 
                           fontsize=7, fontweight='bold', color='red')
                    ax.text(x, y - 0.3, display_planets[2], ha='center', va='center', 
                           fontsize=7, fontweight='bold', color='red')
                
                # 如果有更多行星，显示省略号
                if len(planets_in_house) > 3:
                    ax.text(x + 0.5, y - 0.5, f"+{len(planets_in_house) - 3}", 
                           ha='center', va='center', fontsize=6, color='blue')
        
        # 显示上升星座信息
        asc_info = vedic_data.get('ascendant', {})
        if asc_info:
            asc_sign = asc_info.get('sign', '')
            asc_degree = asc_info.get('degree', 0)
            if asc_sign:
                ax.text(0, 4.5, f"上升: {asc_sign} {asc_degree:.1f}°", 
                       ha='center', va='center', fontsize=12, fontweight='bold',
                       bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.8))
        
        # 在底部显示行星位置摘要（分行显示避免重叠）
        if planets_data:
            planet_info_lines = []
            planet_list = []
            
            for planet, info in list(planets_data.items())[:8]:  # 显示前8个行星
                if isinstance(info, dict):
                    sign = info.get('sign', '')
                    house = info.get('house', '')
                    planet_abbr = {
                        'Sun': '☉', 'Moon': '☽', 'Mercury': '☿', 'Venus': '♀',
                        'Mars': '♂', 'Jupiter': '♃', 'Saturn': '♄', 
                        'Rahu': 'Ra', 'Ketu': 'Ke'
                    }.get(planet, planet[:2])
                    
                    planet_list.append(f"{planet_abbr}:{sign[:3]}-{house}宫")
            
            # 分成两行显示
            if planet_list:
                mid = len(planet_list) // 2
                line1 = " ".join(planet_list[:mid])
                line2 = " ".join(planet_list[mid:])
                
                ax.text(0, -4.8, line1, ha='center', va='center', fontsize=9)
                if line2:
                    ax.text(0, -5.2, line2, ha='center', va='center', fontsize=9)
        
        # 图例（分行显示）
        legend_line1 = "☉太阳 ☽月亮 ☿水星 ♀金星 ♂火星 ♃木星 ♄土星"
        legend_line2 = "Su=Sun Mo=Moon Me=Mercury Ve=Venus Ma=Mars Ju=Jupiter Sa=Saturn"
        
        ax.text(0, -5.8, legend_line1, ha='center', va='center', fontsize=8, style='italic')
        ax.text(0, -6.1, legend_line2, ha='center', va='center', fontsize=7, style='italic')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✅ 印度星盘图已保存: {save_path}")
        else:
            plt.show()
        
        plt.close()
    
    def generate_all_charts(self, output_dir=None):
        """生成所有图表"""
        if output_dir is None:
            output_dir = Path(self.json_file).parent
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(exist_ok=True)
        
        # 获取基础文件名
        base_name = Path(self.json_file).stem
        
        # 生成各种图表
        bazi_path = output_dir / f"{base_name}_八字排盘图.png"
        ziwei_path = output_dir / f"{base_name}_紫微斗数命盘图.png"
        vedic_path = output_dir / f"{base_name}_印度星盘图.png"
        
        self.generate_bazi_chart(bazi_path)
        self.generate_ziwei_chart(ziwei_path)
        self.generate_vedic_chart(vedic_path)
        
        print(f"\n🎉 所有图表生成完成！")
        print(f"📁 输出目录: {output_dir}")
        return [bazi_path, ziwei_path, vedic_path]

def main():
    parser = argparse.ArgumentParser(description='命理图表可视化工具')
    parser.add_argument('json_file', help='JSON排盘数据文件路径')
    parser.add_argument('--output-dir', '-o', help='输出目录（默认为JSON文件所在目录）')
    parser.add_argument('--chart-type', '-t', 
                       choices=['bazi', 'ziwei', 'vedic', 'all'], 
                       default='all',
                       help='生成的图表类型（默认：all）')
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    if not Path(args.json_file).exists():
        print(f"❌ 文件不存在: {args.json_file}")
        sys.exit(1)
    
    print(f"📊 开始处理文件: {args.json_file}")
    
    # 创建可视化器
    visualizer = ChartVisualizer(args.json_file)
    
    # 设置输出目录
    output_dir = Path(args.output_dir) if args.output_dir else Path(args.json_file).parent
    output_dir.mkdir(exist_ok=True)
    base_name = Path(args.json_file).stem
    
    # 根据选择生成图表
    if args.chart_type == 'all':
        visualizer.generate_all_charts(output_dir)
    elif args.chart_type == 'bazi':
        bazi_path = output_dir / f"{base_name}_八字排盘图.png"
        visualizer.generate_bazi_chart(bazi_path)
    elif args.chart_type == 'ziwei':
        ziwei_path = output_dir / f"{base_name}_紫微斗数命盘图.png"
        visualizer.generate_ziwei_chart(ziwei_path)
    elif args.chart_type == 'vedic':
        vedic_path = output_dir / f"{base_name}_印度星盘图.png"
        visualizer.generate_vedic_chart(vedic_path)

if __name__ == '__main__':
    main() 