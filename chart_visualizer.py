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
        """生成印度星盘图（北印度样式）"""
        print("🎨 生成印度星盘图...")
        
        fig, ax = plt.subplots(1, 1, figsize=(10, 10))
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.axis('off')
        ax.set_aspect('equal')
        
        # 标题
        birth_info = self.data['input']
        title = f"D1 North India Chart - {birth_info['birth_date']} {birth_info['birth_time']}"
        ax.text(0, -4.5, title, ha='center', va='center', fontsize=14, fontweight='bold')
        
        # 北印度样式：正方形布局，不是菱形
        square_size = 3
        
        # 绘制外框 - 正方形
        ax.plot([-square_size, square_size], [square_size, square_size], 'k-', linewidth=2)    # 上边
        ax.plot([square_size, square_size], [square_size, -square_size], 'k-', linewidth=2)    # 右边
        ax.plot([square_size, -square_size], [-square_size, -square_size], 'k-', linewidth=2)  # 下边
        ax.plot([-square_size, -square_size], [-square_size, square_size], 'k-', linewidth=2)  # 左边
        
        # 绘制内部分割线形成12个区域
        # 水平分割线
        ax.plot([-square_size, square_size], [1, 1], 'k-', linewidth=1)      # 上1/3线
        ax.plot([-square_size, square_size], [-1, -1], 'k-', linewidth=1)    # 下1/3线
        
        # 垂直分割线
        ax.plot([-1, -1], [-square_size, square_size], 'k-', linewidth=1)    # 左1/3线
        ax.plot([1, 1], [-square_size, square_size], 'k-', linewidth=1)      # 右1/3线
        
        # 对角分割线（形成三角形区域）
        ax.plot([-square_size, -1], [square_size, 1], 'k-', linewidth=1)     # 左上角对角线
        ax.plot([1, square_size], [square_size, 1], 'k-', linewidth=1)       # 右上角对角线
        ax.plot([square_size, 1], [-square_size, -1], 'k-', linewidth=1)     # 右下角对角线
        ax.plot([-1, -square_size], [-square_size, -1], 'k-', linewidth=1)   # 左下角对角线
        
        # 12宫位置定义（按照您的图片布局）
        house_positions = {
            1: (0, 2),          # 第1宫 - 上中（牡羊座）
            2: (-2, 2),         # 第2宫 - 左上角（金牛座）
            3: (-2, 0),         # 第3宫 - 左中（双子座）
            4: (-2, -2),        # 第4宫 - 左下角（巨蟹座）
            5: (0, -2),         # 第5宫 - 下中（狮子座）
            6: (2, -2),         # 第6宫 - 右下角（处女座）
            7: (2, 0),          # 第7宫 - 右中（天秤座）
            8: (2, 2),          # 第8宫 - 右上角（天蝎座）
            9: (-0.5, 0.5),     # 第9宫 - 中左上（射手座）
            10: (-0.5, -0.5),   # 第10宫 - 中左下（摩羯座）
            11: (0.5, -0.5),    # 第11宫 - 中右下（水瓶座）
            12: (0.5, 0.5)      # 第12宫 - 中右上（双鱼座）
        }
        
        # 星座中文名称映射
        sign_chinese = {
            'Aries': '白羊座', 'Taurus': '金牛座', 'Gemini': '双子座', 'Cancer': '巨蟹座',
            'Leo': '狮子座', 'Virgo': '处女座', 'Libra': '天秤座', 'Scorpio': '天蝎座',
            'Sagittarius': '射手座', 'Capricorn': '摩羯座', 'Aquarius': '水瓶座', 'Pisces': '双鱼座'
        }
        
        # 行星中文名称映射
        planet_chinese = {
            'Sun': '日', 'Moon': '月', 'Mercury': '水', 'Venus': '金',
            'Mars': '火', 'Jupiter': '木', 'Saturn': '土', 
            'Rahu': 'Ra', 'Ketu': 'Ke', 'Uranus': '天', 'Neptune': '海', 'Pluto': '冥'
        }
        
        # 获取印度星盘数据
        vedic_data = self.data.get('vedic', {})
        planets_data = vedic_data.get('planets', {})
        houses_data = vedic_data.get('houses', {})
        
        # 获取上升星座
        asc_info = vedic_data.get('ascendant', {})
        asc_sign = asc_info.get('sign', 'Aries') if asc_info else 'Aries'
        
        # 计算每个宫位对应的星座（从上升星座开始）
        signs_order = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                      'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        try:
            asc_index = signs_order.index(asc_sign)
        except ValueError:
            asc_index = 0  # 默认从白羊座开始
        
        # 为每个宫位分配星座和收集行星
        house_signs = {}
        house_planets = {i: [] for i in range(1, 13)}
        
        for house_num in range(1, 13):
            sign_index = (asc_index + house_num - 1) % 12
            house_signs[house_num] = signs_order[sign_index]
        
        # 分析行星在各宫位的分布
        for planet_name, planet_info in planets_data.items():
            if isinstance(planet_info, dict):
                house_num = planet_info.get('house')
                if house_num and 1 <= house_num <= 12:
                    planet_abbr = planet_chinese.get(planet_name, planet_name)
                    degree = planet_info.get('lon', 0)  # 使用lon字段作为角度
                    house_planets[house_num].append(f"{planet_abbr} {degree:.1f}")
        
        # 绘制各宫位信息
        for house_num in range(1, 13):
            x, y = house_positions[house_num]
            sign_name = house_signs[house_num]
            sign_chinese_name = sign_chinese.get(sign_name, sign_name)
            
            # 显示星座名称
            ax.text(x, y + 0.3, sign_chinese_name, ha='center', va='center', 
                   fontsize=9, fontweight='bold', color='black')
            
            # 显示该宫位的行星（带角度）
            planets_in_house = house_planets[house_num]
            if planets_in_house:
                if len(planets_in_house) == 1:
                    # 单个行星
                    ax.text(x, y - 0.2, planets_in_house[0], ha='center', va='center', 
                           fontsize=8, color='blue')
                elif len(planets_in_house) == 2:
                    # 两个行星
                    ax.text(x, y - 0.1, planets_in_house[0], ha='center', va='center', 
                           fontsize=7, color='blue')
                    ax.text(x, y - 0.35, planets_in_house[1], ha='center', va='center', 
                           fontsize=7, color='blue')
                else:
                    # 多个行星，紧凑显示
                    for i, planet in enumerate(planets_in_house[:3]):
                        ax.text(x, y - 0.05 - i * 0.12, planet, ha='center', va='center', 
                               fontsize=6, color='blue')
                    if len(planets_in_house) > 3:
                        ax.text(x + 0.3, y - 0.3, f"+{len(planets_in_house) - 3}", 
                               ha='center', va='center', fontsize=5, color='red')
        
        # 在第1宫添加Lagna标记
        lagna_x, lagna_y = house_positions[1]
        ax.text(lagna_x, lagna_y, "Lagna", ha='center', va='center', 
               fontsize=7, fontweight='bold', color='blue',
               bbox=dict(boxstyle="round,pad=0.1", facecolor='lightblue', alpha=0.8))
        
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