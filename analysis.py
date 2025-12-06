"""
SaaS MRR Growth Analysis
Senior Data Analyst: 24f3004473@ds.study.iitm.ac.in
Date: December 7, 2025

This script analyzes quarterly MRR growth data and generates visualizations
to support strategic decision-making.

Analysis completed using ChatGPT Codex: https://chatgpt.com/codex/tasks
"""

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style for professional visualizations
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

def load_data(filepath='data.json'):
    """Load quarterly MRR growth data from JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def calculate_statistics(mrr_data):
    """Calculate key statistics from MRR growth data."""
    values = list(mrr_data.values())
    
    stats = {
        'average': round(np.mean(values), 2),
        'median': round(np.median(values), 2),
        'std_dev': round(np.std(values), 2),
        'min': min(values),
        'max': max(values),
        'range': round(max(values) - min(values), 2)
    }
    
    return stats

def analyze_trend(mrr_data):
    """Analyze the trend in MRR growth across quarters."""
    quarters = list(mrr_data.keys())
    values = list(mrr_data.values())
    
    # Calculate quarter-over-quarter changes
    qoq_changes = []
    for i in range(1, len(values)):
        change = values[i] - values[i-1]
        qoq_changes.append({
            'from': quarters[i-1],
            'to': quarters[i],
            'change': round(change, 2),
            'percent_change': round((change / values[i-1]) * 100, 2)
        })
    
    return qoq_changes

def create_visualizations(data, stats, output_dir='visualizations'):
    """Create comprehensive visualizations for the data story."""
    Path(output_dir).mkdir(exist_ok=True)
    
    mrr_data = data['mrr_growth']
    target = data['industry_target']
    quarters = list(mrr_data.keys())
    values = list(mrr_data.values())
    
    # Visualization 1: Quarterly MRR Growth Trend with Benchmark
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Plot actual MRR growth
    ax.plot(quarters, values, marker='o', linewidth=3, markersize=10, 
            color='#2E86AB', label='Actual MRR Growth', zorder=3)
    
    # Plot industry target line
    ax.axhline(y=target, color='#A23B72', linestyle='--', linewidth=2, 
               label=f'Industry Target ({target}%)', zorder=2)
    
    # Plot average line
    ax.axhline(y=stats['average'], color='#F18F01', linestyle=':', linewidth=2, 
               label=f'Current Average ({stats["average"]}%)', zorder=2)
    
    # Add value labels on data points
    for i, (q, v) in enumerate(zip(quarters, values)):
        ax.annotate(f'{v}%', xy=(i, v), xytext=(0, 10), 
                   textcoords='offset points', ha='center', fontsize=11, 
                   fontweight='bold', color='#2E86AB')
    
    # Fill the gap between actual and target
    ax.fill_between(range(len(quarters)), values, target, 
                    where=[v < target for v in values], 
                    alpha=0.2, color='red', label='Performance Gap')
    
    ax.set_xlabel('Quarter (2024)', fontsize=13, fontweight='bold')
    ax.set_ylabel('MRR Growth Rate (%)', fontsize=13, fontweight='bold')
    ax.set_title('SaaS Company: Quarterly MRR Growth vs Industry Benchmark\n' + 
                 'Performance Gap Analysis - 2024', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(0, 18)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/mrr_trend_analysis.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/mrr_trend_analysis.png")
    plt.close()
    
    # Visualization 2: Performance Gap Analysis
    fig, ax = plt.subplots(figsize=(12, 7))
    
    gaps = [target - v for v in values]
    colors = ['#E63946' if gap > 0 else '#06A77D' for gap in gaps]
    
    bars = ax.bar(quarters, gaps, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add value labels
    for i, (bar, gap) in enumerate(zip(bars, gaps)):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{gap:.2f}%',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=12, fontweight='bold')
    
    ax.axhline(y=0, color='black', linewidth=1)
    ax.set_xlabel('Quarter (2024)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Gap from Target (%)', fontsize=13, fontweight='bold')
    ax.set_title('MRR Growth Gap Analysis: Distance from Industry Target (15%)\n' +
                 'Negative values indicate underperformance',
                 fontsize=16, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3, axis='y')
    
    # Add average gap annotation
    avg_gap = np.mean(gaps)
    ax.text(0.98, 0.95, f'Average Gap: {avg_gap:.2f}%\nTarget: Reduce to 0%',
            transform=ax.transAxes, fontsize=12,
            verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/performance_gap.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/performance_gap.png")
    plt.close()
    
    # Visualization 3: Quarterly Comparison Dashboard
    fig = plt.figure(figsize=(14, 10))
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # Subplot 1: Bar chart comparison
    ax1 = fig.add_subplot(gs[0, :])
    x_pos = np.arange(len(quarters))
    width = 0.35
    
    ax1.bar(x_pos - width/2, values, width, label='Actual', color='#2E86AB', alpha=0.8)
    ax1.bar(x_pos + width/2, [target]*len(quarters), width, label='Target', 
            color='#A23B72', alpha=0.8)
    
    ax1.set_xlabel('Quarter', fontweight='bold')
    ax1.set_ylabel('MRR Growth (%)', fontweight='bold')
    ax1.set_title('Actual vs Target MRR Growth by Quarter', fontweight='bold', fontsize=14)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(quarters)
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # Subplot 2: Statistics summary
    ax2 = fig.add_subplot(gs[1, 0])
    ax2.axis('off')
    
    stats_text = f"""
    KEY STATISTICS (2024)
    
    Average MRR Growth:    {stats['average']}%
    Industry Target:       {target}%
    Gap to Target:         {round(target - stats['average'], 2)}%
    
    Median Growth:         {stats['median']}%
    Standard Deviation:    {stats['std_dev']}%
    Range:                 {stats['min']}% - {stats['max']}%
    
    Best Quarter:          Q4 ({max(values)}%)
    Worst Quarter:         Q1 ({min(values)}%)
    """
    
    ax2.text(0.1, 0.9, stats_text, transform=ax2.transAxes,
             fontsize=11, verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Subplot 3: Quarter-over-Quarter changes
    ax3 = fig.add_subplot(gs[1, 1])
    qoq_labels = ['Q1→Q2', 'Q2→Q3', 'Q3→Q4']
    qoq_values = [values[i+1] - values[i] for i in range(len(values)-1)]
    qoq_colors = ['#06A77D' if v > 0 else '#E63946' for v in qoq_values]
    
    ax3.bar(qoq_labels, qoq_values, color=qoq_colors, alpha=0.7)
    ax3.axhline(y=0, color='black', linewidth=1)
    ax3.set_ylabel('Change in Growth Rate (%)', fontweight='bold')
    ax3.set_title('Quarter-over-Quarter Change', fontweight='bold')
    ax3.grid(True, alpha=0.3, axis='y')
    
    for i, v in enumerate(qoq_values):
        ax3.text(i, v, f'{v:+.2f}%', ha='center', 
                va='bottom' if v > 0 else 'top', fontweight='bold')
    
    # Subplot 4: Achievement Rate
    ax4 = fig.add_subplot(gs[2, :])
    achievement_rates = [(v/target)*100 for v in values]
    
    ax4.plot(quarters, achievement_rates, marker='s', linewidth=3, markersize=12,
            color='#F18F01')
    ax4.axhline(y=100, color='green', linestyle='--', linewidth=2, 
               label='100% Achievement (Target)')
    ax4.fill_between(range(len(quarters)), achievement_rates, 100,
                     where=[r < 100 for r in achievement_rates],
                     alpha=0.2, color='red')
    
    for i, (q, r) in enumerate(zip(quarters, achievement_rates)):
        ax4.annotate(f'{r:.1f}%', xy=(i, r), xytext=(0, -15),
                    textcoords='offset points', ha='center', fontsize=10,
                    fontweight='bold')
    
    ax4.set_xlabel('Quarter', fontweight='bold')
    ax4.set_ylabel('Target Achievement Rate (%)', fontweight='bold')
    ax4.set_title('Quarterly Achievement Rate vs Industry Target', fontweight='bold', fontsize=14)
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(40, 110)
    
    plt.suptitle('SaaS MRR Growth Performance Dashboard - 2024', 
                fontsize=16, fontweight='bold', y=0.995)
    
    plt.savefig(f'{output_dir}/comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {output_dir}/comprehensive_dashboard.png")
    plt.close()

def generate_report(data, stats, qoq_changes):
    """Generate text report with key insights."""
    mrr_data = data['mrr_growth']
    target = data['industry_target']
    
    report = f"""
    ============================================================
    SaaS MRR GROWTH ANALYSIS REPORT
    ============================================================
    Analyst: {data['analyst_email']}
    Report Date: December 7, 2025
    Analysis Period: {data['year']} (Quarterly)
    ============================================================
    
    EXECUTIVE SUMMARY
    ------------------------------------------------------------
    Current Average MRR Growth: {stats['average']}%
    Industry Target:            {target}%
    Performance Gap:            {round(target - stats['average'], 2)}%
    Achievement Rate:           {round((stats['average']/target)*100, 1)}%
    
    KEY FINDINGS
    ------------------------------------------------------------
    1. The company is underperforming the industry benchmark by 
       {round(target - stats['average'], 2)} percentage points.
    
    2. Q4 showed the strongest performance at {mrr_data['Q4']}%, but 
       still fell short of the {target}% target.
    
    3. Growth volatility (std dev: {stats['std_dev']}%) indicates 
       inconsistent performance across quarters.
    
    4. All quarters in 2024 failed to meet the industry target,
       with Q1 showing the weakest performance at {mrr_data['Q1']}%.
    
    QUARTER-OVER-QUARTER ANALYSIS
    ------------------------------------------------------------
    """
    
    for change in qoq_changes:
        direction = "↑" if change['change'] > 0 else "↓"
        report += f"{change['from']} → {change['to']}: {direction} {abs(change['change'])}% "
        report += f"({change['percent_change']:+.1f}%)\n    "
    
    report += f"""
    
    STRATEGIC RECOMMENDATIONS
    ------------------------------------------------------------
    To reach the {target}% target, the company must:
    
    1. EXPAND INTO NEW MARKET SEGMENTS
       - Identify high-growth verticals
       - Develop market-specific value propositions
       - Allocate resources to market expansion
    
    2. Improve product-market fit in existing segments
    3. Enhance customer acquisition strategies
    4. Optimize pricing and packaging
    5. Strengthen customer retention programs
    
    ============================================================
    """
    
    return report

def main():
    """Main analysis workflow."""
    print("\n" + "="*60)
    print("SaaS MRR GROWTH ANALYSIS")
    print("="*60 + "\n")
    
    # Load data
    print("Loading data...")
    data = load_data()
    print(f"✓ Data loaded for {data['year']}")
    print(f"✓ Analyst: {data['analyst_email']}\n")
    
    # Calculate statistics
    print("Calculating statistics...")
    stats = calculate_statistics(data['mrr_growth'])
    print(f"✓ Average MRR Growth: {stats['average']}%")
    print(f"✓ Target: {data['industry_target']}%")
    print(f"✓ Gap: {round(data['industry_target'] - stats['average'], 2)}%\n")
    
    # Analyze trends
    print("Analyzing trends...")
    qoq_changes = analyze_trend(data['mrr_growth'])
    print(f"✓ Analyzed {len(qoq_changes)} quarter-over-quarter changes\n")
    
    # Create visualizations
    print("Creating visualizations...")
    create_visualizations(data, stats)
    print()
    
    # Generate report
    print("Generating report...")
    report = generate_report(data, stats, qoq_changes)
    
    with open('analysis_report.txt', 'w', encoding='utf-8') as f:
        f.write(report)
    print("✓ Saved: analysis_report.txt\n")
    
    print(report)
    
    print("="*60)
    print("ANALYSIS COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
