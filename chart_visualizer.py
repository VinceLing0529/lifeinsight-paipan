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
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.axis('off')
        ax.set_aspect('equal')
        
        # 标题
        birth_info = self.data['input']
        title = f"印度星盘 (Vedic Chart) - {birth_info['birth_date']} {birth_info['birth_time']}"
        ax.text(0, 4.5, title, ha='center', va='center', fontsize=14, fontweight='bold')
        
        # 南印度样式：菱形12宫布局
        # 绘制外框
        outer_square = Rectangle((-3, -3), 6, 6, facecolor='none', edgecolor='black', linewidth=2)
        ax.add_patch(outer_square)
        
        # 绘制内部分割线
        # 水平线
        ax.plot([-3, 3], [1, 1], 'k-', linewidth=1)
        ax.plot([-3, 3], [-1, -1], 'k-', linewidth=1)
        # 垂直线
        ax.plot([-1, -1], [-3, 3], 'k-', linewidth=1)
        ax.plot([1, 1], [-3, 3], 'k-', linewidth=1)
        
        # 对角线
        ax.plot([-3, -1], [3, 1], 'k-', linewidth=1)
        ax.plot([1, 3], [3, 1], 'k-', linewidth=1)
        ax.plot([-3, -1], [-3, -1], 'k-', linewidth=1)
        ax.plot([1, 3], [-3, -1], 'k-', linewidth=1)
        
        # 12宫位置定义（南印度样式）
        house_positions = {
            1: (0, 2),      # 第1宫（上中）
            2: (2, 2),      # 第2宫（右上）
            3: (2, 0),      # 第3宫（右中）
            4: (2, -2),     # 第4宫（右下）
            5: (0, -2),     # 第5宫（下中）
            6: (-2, -2),    # 第6宫（左下）
            7: (-2, 0),     # 第7宫（左中）
            8: (-2, 2),     # 第8宫（左上）
            9: (-2, 0),     # 第9宫
            10: (0, 2),     # 第10宫
            11: (2, 0),     # 第11宫
            12: (0, -2)     # 第12宫
        }
        
        # 宫位名称
        house_names = {
            1: "Asc", 2: "2nd", 3: "3rd", 4: "4th",
            5: "5th", 6: "6th", 7: "7th", 8: "8th",
            9: "9th", 10: "10th", 11: "11th", 12: "12th"
        }
        
        # 星座符号映射
        sign_symbols = {
            'Aries': '♈', 'Taurus': '♉', 'Gemini': '♊', 'Cancer': '♋',
            'Leo': '♌', 'Virgo': '♍', 'Libra': '♎', 'Scorpio': '♏',
            'Sagittarius': '♐', 'Capricorn': '♑', 'Aquarius': '♒', 'Pisces': '♓'
        }
        
        # 行星符号映射
        planet_symbols = {
            'Sun': '☉', 'Moon': '☽', 'Mercury': '☿', 'Venus': '♀',
            'Mars': '♂', 'Jupiter': '♃', 'Saturn': '♄', 'Uranus': '♅',
            'Neptune': '♆', 'Pluto': '♇', 'Rahu': '☊', 'Ketu': '☋'
        }
        
        # 获取印度星盘数据
        vedic_data = self.data.get('vedic', {})
        
        # 绘制各宫位信息
        for house_num in range(1, 13):
            if house_num in house_positions:
                x, y = house_positions[house_num]
                
                # 宫位编号
                ax.text(x, y+0.6, house_names[house_num], ha='center', va='center', 
                       fontsize=8, fontweight='bold')
                
                # 这里需要根据实际的vedic数据结构来填充
                # 由于当前vedic数据结构比较复杂，我们先显示基本信息
                
                # 示例：显示一些基本信息
                if house_num == 1:  # 上升星座
                    asc_info = vedic_data.get('houses', {}).get('1', {})
                    if asc_info:
                        ax.text(x, y, "ASC", ha='center', va='center', 
                               fontsize=10, fontweight='bold', color='red')
        
        # 在图表底部显示行星位置信息
        planets_info = vedic_data.get('planets', {})
        if planets_info:
            info_text = "行星位置: "
            planet_list = []
            for planet, info in list(planets_info.items())[:6]:  # 显示前6个行星
                if isinstance(info, dict):
                    sign = info.get('sign', '')
                    symbol = planet_symbols.get(planet, planet[:2])
                    planet_list.append(f"{symbol}({sign[:3]})")
            
            if planet_list:
                info_text += " ".join(planet_list)
                ax.text(0, -4, info_text, ha='center', va='center', fontsize=9)
        
        # 图例
        legend_text = "ASC=上升点 ☉=太阳 ☽=月亮 ☿=水星 ♀=金星 ♂=火星 ♃=木星 ♄=土星"
        ax.text(0, -4.5, legend_text, ha='center', va='center', fontsize=8, style='italic')
        
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