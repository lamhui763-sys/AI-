"""
Data Module Usage Examples
数据模块使用示例

演示如何使用数据获取、处理和管理功能

Author: WorkBuddy AI
Date: 2026-03-12
"""

import sys
import os

# 添加项目路径
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

import yaml
from ai_inv.data_manager import DataManager


def example_1_basic_fetch():
    """示例1: 基本数据获取"""
    print("=" * 80)
    print("示例1: 获取港股数据")
    print("=" * 80)

    # 加载配置
    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'hk_stocks': {
            'watchlist': ['6158.HK', '7200.HK', '^HSI'],
            'default_period': '1y',
            'default_interval': '1d'
        },
        'database': {'path': './examples/data/investment.db'}
    }

    # 初始化数据管理器
    data_manager = DataManager(config)

    # 获取单只股票数据
    symbol = '6158.HK'  # 正荣控股
    data = data_manager.get_stock_data(symbol, period='1y', interval='1d')

    if data is not None:
        print(f"\n成功获取 {symbol} 的数据:")
        print(f"- 数据记录数: {len(data)}")
        print(f"- 日期范围: {data.index.min().strftime('%Y-%m-%d')} 至 {data.index.max().strftime('%Y-%m-%d')}")
        print(f"- 当前价格: HKD {data['Close'].iloc[-1]:.2f}")
        print(f"- 最高价: HKD {data['High'].max():.2f}")
        print(f"- 最低价: HKD {data['Low'].min():.2f}")
        print(f"- 平均成交量: {data['Volume'].mean():.0f}")

        # 显示最后5条记录
        print(f"\n最近5个交易日数据:")
        print(data.tail(5)[['Open', 'High', 'Low', 'Close', 'Volume']])
    else:
        print(f"\n无法获取 {symbol} 的数据")


def example_2_multiple_stocks():
    """示例2: 获取多只股票数据"""
    print("\n" + "=" * 80)
    print("示例2: 获取关注列表数据")
    print("=" * 80)

    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'hk_stocks': {
            'watchlist': ['6158.HK', '7200.HK', '^HSI'],
            'default_period': '6m',
            'default_interval': '1d'
        },
        'database': {'path': './examples/data/investment.db'}
    }

    data_manager = DataManager(config)

    # 获取关注列表数据
    results = data_manager.get_watchlist_data()

    print(f"\n成功获取 {len(results)} 只股票的数据:")
    for symbol, data in results.items():
        print(f"\n{symbol}:")
        print(f"  - 数据记录数: {len(data)}")
        print(f"  - 当前价格: {data['Close'].iloc[-1]:.2f}")
        print(f"  - 近期涨跌幅: {(data['Close'].iloc[-1] / data['Close'].iloc[-5] - 1) * 100:.2f}%")


def example_3_data_summary():
    """示例3: 数据摘要和质量检查"""
    print("\n" + "=" * 80)
    print("示例3: 数据摘要和质量检查")
    print("=" * 80)

    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'database': {'path': './examples/data/investment.db'}
    }

    data_manager = DataManager(config)

    # 获取数据摘要
    symbol = '6158.HK'
    summary = data_manager.get_data_summary(symbol)

    if summary is not None:
        print(f"\n{symbol} 数据摘要:")
        print(f"\n数据质量:")
        quality = summary['data_quality']
        print(f"  - 完整性: {quality['completeness']}%")
        print(f"  - 新鲜度: {quality['freshness']['status']} (最后日期: {quality['freshness']['last_date']})")
        print(f"  - 一致性: {quality['consistency']['overall']}")

        print(f"\n价格统计:")
        price_stats = summary['statistics']['price_stats']
        print(f"  - 均值: {price_stats['mean']:.2f}")
        print(f"  - 中位数: {price_stats['median']:.2f}")
        print(f"  - 标准差: {price_stats['std']:.2f}")
        print(f"  - 最小值: {price_stats['min']:.2f}")
        print(f"  - 最大值: {price_stats['max']:.2f}")

        print(f"\n收益率统计:")
        returns_stats = summary['statistics']['returns_stats']
        print(f"  - 平均收益率: {returns_stats['mean']*100:.2f}%")
        print(f"  - 收益率标准差: {returns_stats['std']*100:.2f}%")
        print(f"  - 偏度: {returns_stats['skewness']:.2f}")
        print(f"  - 峰度: {returns_stats['kurtosis']:.2f}")


def example_4_historical_data():
    """示例4: 获取历史数据（用于回测）"""
    print("\n" + "=" * 80)
    print("示例4: 获取历史数据")
    print("=" * 80)

    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'database': {'path': './examples/data/investment.db'}
    }

    data_manager = DataManager(config)

    # 获取特定历史期间的数据
    symbol = '^HSI'
    start_date = '2023-01-01'
    end_date = '2024-01-01'

    data = data_manager.get_historical_data(symbol, start_date, end_date)

    if data is not None:
        print(f"\n{symbol} 历史数据 ({start_date} 至 {end_date}):")
        print(f"- 数据记录数: {len(data)}")
        print(f"- 期间收益率: {(data['Close'].iloc[-1] / data['Close'].iloc[0] - 1) * 100:.2f}%")
        print(f"- 期间最高点: {data['High'].max():.2f}")
        print(f"- 期间最低点: {data['Low'].min():.2f}")
        print(f"- 期间波动率: {data['returns'].std()*100:.2f}%")


def example_5_export_data():
    """示例5: 导出数据"""
    print("\n" + "=" * 80)
    print("示例5: 导出数据到Excel")
    print("=" * 80)

    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'database': {'path': './examples/data/investment.db'}
    }

    data_manager = DataManager(config)

    # 导出Excel
    symbol = '6158.HK'
    excel_file = data_manager.export_data(symbol, format='excel')

    if excel_file:
        print(f"\n成功导出 {symbol} 数据到:")
        print(f"文件路径: {excel_file}")

    # 导出CSV
    csv_file = data_manager.export_data(symbol, format='csv')

    if csv_file:
        print(f"\n成功导出 {symbol} 数据到:")
        print(f"文件路径: {csv_file}")


def example_6_cache_management():
    """示例6: 缓存管理"""
    print("\n" + "=" * 80)
    print("示例6: 缓存管理")
    print("=" * 80)

    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'database': {'path': './examples/data/investment.db'}
    }

    data_manager = DataManager(config)

    symbol = '6158.HK'

    # 第一次获取（从网络）
    print("\n第一次获取数据（从网络）:")
    data = data_manager.get_stock_data(symbol, use_cache=True)
    if data is not None:
        print(f"- 成功获取 {len(data)} 条记录")

    # 第二次获取（从缓存）
    print("\n第二次获取数据（从缓存）:")
    data = data_manager.get_stock_data(symbol, use_cache=True)
    if data is not None:
        print(f"- 成功获取 {len(data)} 条记录（使用缓存）")

    # 强制刷新
    print("\n强制刷新缓存:")
    data = data_manager.get_stock_data(symbol, force_refresh=True)
    if data is not None:
        print(f"- 成功获取 {len(data)} 条记录（网络刷新）")


def example_7_data_maintenance():
    """示例7: 数据维护"""
    print("\n" + "=" * 80)
    print("示例7: 数据维护")
    print("=" * 80)

    config = {
        'yahoo_finance': {'enabled': True, 'timeout': 30},
        'database': {
            'path': './examples/data/investment.db',
            'backup_enabled': True
        }
    }

    data_manager = DataManager(config)

    # 执行维护任务
    print("\n执行数据维护:")
    data_manager.maintenance()

    print("\n维护任务完成:")
    print("- 数据库已备份")
    print("- 旧数据已清理（保留365天）")


def main():
    """运行所有示例"""
    print("\n" + "=" * 80)
    print("AI Investment Tool - Data Module Examples")
    print("=" * 80)

    try:
        # 创建输出目录
        import os
        os.makedirs('./examples/data', exist_ok=True)
        os.makedirs('./examples/output', exist_ok=True)

        # 运行示例
        example_1_basic_fetch()
        example_2_multiple_stocks()
        example_3_data_summary()
        example_4_historical_data()
        example_5_export_data()
        example_6_cache_management()
        example_7_data_maintenance()

        print("\n" + "=" * 80)
        print("所有示例运行完成！")
        print("=" * 80)

    except Exception as e:
        print(f"\n错误: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
