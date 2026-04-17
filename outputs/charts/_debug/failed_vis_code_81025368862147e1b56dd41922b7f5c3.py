0001: import matplotlib as mpl
0002: import matplotlib.pyplot as plt
0003: import matplotlib.gridspec as gridspec
0004: palette = ['#0057b8', '#ffb400', '#ef3340', '#8fc93a', '#342e37']
0005: bg_color = '#fcfcfc'
0006: border_color = '#d0d0d0'
0007: sparkline_color = '#8fc93a'
0008: title_font = {'fontsize': 26, 'fontweight': 'bold', 'color': '#202020'}
0009: label_font = {'fontsize': 16, 'fontweight': 'bold', 'color': '#505050'}
0010: value_font = {'fontsize': 32, 'fontweight': 'semibold', 'color': '#222'}
0011: state_font = {'fontsize': 17, 'fontweight': 'regular', 'color': '#777'}
0012: small_font = {'fontsize': 13, 'color': '#888'}
0013: kpi_labels = ['Churn Rate', 'Active Member Rate', 'High-Balance Rate', 'Multi-Product Rate']
0014: kpi_values = [20.37, 51.51, 49.98, 38.69]
0015: kpi_states = ['Detractors', 'Passives', 'Promoters', 'Promoters']
0016: spark_churn = np.array([16, 18, 20, 21, 20.4, 21, 20.3, 19.6, 21, 20.7])
0017: spark_active = np.array([49.7, 52.3, 53.5, 51.0, 50.2, 52.1, 51.6, 52, 54, 51.51])
0018: spark_balance = np.array([47, 50, 52, 49.9, 50.1, 51.2, 49.86, 51.0, 50.3, 49.98])
0019: spark_product = np.array([36, 37.8, 39.2, 38.5, 39, 38.9, 38.2, 39.1, 38.7, 38.69])
0020: gauge1_val = 20.37
0021: gauge1_lab = 'Churn Rate'
0022: gauge2_val = 51.51
0023: gauge2_lab = 'Active Member Rate'
0024: trend_age_labels = ['<30', '30-44', '45+']
0025: trend_age_vals = [14.0, 18.5, 27.3]
0026: country_names = ['France', 'Germany', 'Spain']
0027: country_total = np.array([5014, 2509, 2477])
0028: country_churn_rate = np.array([18.7, 22.5, 21.2])
0029: fig = plt.figure(figsize=(19.2, 10.8), constrained_layout=False)
0030: gs = gridspec.GridSpec(3, 6, figure=fig, hspace=0.21, wspace=0.2)
0031: card_pos = [(0, 0), (0, 1), (0, 2), (0, 3)]
0032: spark_data = [spark_churn, spark_active, spark_balance, spark_product]
0033: for (i, pos) in enumerate(card_pos):
0034:     ax = fig.add_subplot(gs[pos[0], pos[1]:pos[1] + 1])
0035:     ax.set_facecolor(bg_color)
0036:     for spine in ax.spines.values():
0037:         spine.set_edgecolor(border_color)
0038:         spine.set_linewidth(1.0)
0039:     ax.text(0.05, 0.68, f'{kpi_values[i]:.2f}%', fontdict=value_font, transform=ax.transAxes, va='center')
0040:     ax.text(0.05, 0.35, kpi_labels[i], fontdict=label_font, transform=ax.transAxes, va='bottom')
0041:     state_icon = {'Promoters': '✪', 'Passives': '⚠', 'Detractors': '❌'}
0042:     ax.text(0.86, 0.72, state_icon.get(kpi_states[i], '?'), fontdict={'fontsize': 22, 'color': '#c1c1c1'}, transform=ax.transAxes, va='center')
0043:     ax.text(0.86, 0.35, kpi_states[i], fontdict=state_font, transform=ax.transAxes, va='bottom', ha='center')
0044:     ax.plot(np.linspace(0.25, 0.95, len(spark_data[i])), spark_data[i], color=sparkline_color, linewidth=2.2, alpha=0.9, transform=ax.transAxes, clip_on=False)
0045:     ax.set_xticks([])
0046:     ax.set_yticks([])
0047:     ax.set_xticklabels([])
0048:     ax.set_yticklabels([])
0049:     ax.set_xlim(0, 1)
0050:     ax.set_ylim(0, 1)
0051:     ax.patch.set_alpha(0.97)
0052:     ax.text(0.02, 0.04, f'10,000 sample', fontdict=small_font, transform=ax.transAxes, va='bottom')
0053: ax = fig.add_subplot(gs[0, 4:6])
0054: ax.set_facecolor(bg_color)
0055: for spine in ax.spines.values():
0056:     spine.set_edgecolor(border_color)
0057:     spine.set_linewidth(1.0)
0058: ax.text(0.5, 0.55, 'Bank Customer Churn Dashboard', fontdict=title_font, va='center', ha='center', transform=ax.transAxes)
0059: ax.axis('off')
0060: ax_g1 = fig.add_subplot(gs[1, 0:2], polar=True)
0061: ax_g1.set_facecolor(bg_color)
0062: for spine in ax_g1.spines.values():
0063:     spine.set_edgecolor(border_color)
0064:     spine.set_linewidth(1.0)
0065: ax_g1.set_theta_offset(np.pi / 2)
0066: ax_g1.set_theta_direction(-1)
0067: v1 = gauge1_val / 100
0068: ax_g1.bar([0], [1], width=2 * np.pi * v1, color=palette[2], alpha=0.85, lw=0)
0069: ax_g1.bar([0], [1], width=2 * np.pi * (1 - v1), color='#f0f0f0', alpha=1, lw=0, bottom=0)
0070: ax_g1.text(0, 0.3, f'{gauge1_val:.2f}%', fontdict=value_font, ha='center', va='bottom', color=palette[2])
0071: ax_g1.text(0, 0.1, gauge1_lab, fontdict=label_font, ha='center', va='top', color=palette[2])
0072: ax_g1.text(np.pi, 0.8, f"{('Detractor' if gauge1_val > 18 else 'Promoter')}", fontdict=state_font, ha='center', va='top')
0073: ax_g1.set_xticks([])
0074: ax_g1.set_yticks([])
0075: ax_g1.grid(False)
0076: ax_g1.set_ylim(0, 1)
0077: ax_g2 = fig.add_subplot(gs[1, 2:4], polar=True)
0078: ax_g2.set_facecolor(bg_color)
0079: for spine in ax_g2.spines.values():
0080:     spine.set_edgecolor(border_color)
0081:     spine.set_linewidth(1.0)
0082: ax_g2.set_theta_offset(np.pi / 2)
0083: ax_g2.set_theta_direction(-1)
0084: v2 = gauge2_val / 100
0085: ax_g2.bar([0], [1], width=2 * np.pi * v2, color=palette[1], alpha=0.85, lw=0)
0086: ax_g2.bar([0], [1], width=2 * np.pi * (1 - v2), color='#f0f0f0', alpha=1, lw=0, bottom=0)
0087: ax_g2.text(0, 0.3, f'{gauge2_val:.2f}%', fontdict=value_font, ha='center', va='bottom', color=palette[1])
0088: ax_g2.text(0, 0.1, gauge2_lab, fontdict=label_font, ha='center', va='top', color=palette[1])
0089: ax_g2.text(np.pi, 0.8, f"{('Promoter' if gauge2_val > 50 else 'Passive')}", fontdict=state_font, ha='center', va='top')
0090: ax_g2.set_xticks([])
0091: ax_g2.set_yticks([])
0092: ax_g2.grid(False)
0093: ax_g2.set_ylim(0, 1)
0094: ax_t = fig.add_subplot(gs[1, 4:6])
0095: ax_t.set_facecolor(bg_color)
0096: for spine in ax_t.spines.values():
0097:     spine.set_edgecolor(border_color)
0098:     spine.set_linewidth(1.0)
0099: ax_t.plot(trend_age_labels, trend_age_vals, marker='o', color=palette[3], linewidth=2)
0100: for (i, v) in enumerate(trend_age_vals):
0101:     if v > 25:
0102:         ax_t.annotate('High churn!', xy=(trend_age_labels[i], v), xytext=(trend_age_labels[i], v + 2), arrowprops=dict(arrowstyle='->', color='#ef3340'), fontdict=small_font)
0103: ax_t.set_title('Churn (%) by Age Group', fontdict=label_font, pad=12)
0104: ax_t.set_xlabel('Age Group', fontdict=small_font)
0105: ax_t.set_ylabel('Churn Rate (%)', fontdict=small_font)
0106: ax_t.set_ylim(10, 30)
0107: ax_t.grid(axis='y', linestyle=':', alpha=0.22)
0108: ax_t.tick_params(axis='x', labelsize=15)
0109: ax_t.tick_params(axis='y', labelsize=15)
0110: ax_b = fig.add_subplot(gs[2, 0:3])
0111: ax_b.set_facecolor(bg_color)
0112: for spine in ax_b.spines.values():
0113:     spine.set_edgecolor(border_color)
0114:     spine.set_linewidth(1.0)
0115: bar1 = ax_b.bar(country_names, country_total, color=palette[0], alpha=0.82, width=0.55, label='Total')
0116: bar2 = ax_b.bar(country_names, country_total * (country_churn_rate / 100), color=palette[2], alpha=0.89, width=0.35, label='Churn')
0117: for (i, v) in enumerate(country_churn_rate):
0118:     ax_b.text(i, country_total[i] * (v / 100) + 150, f'{v:.1f}%', ha='center', va='bottom', fontdict=small_font)
0119: ax_b.set_title('Customer Churn by Country', fontdict=label_font, pad=14)
0120: ax_b.set_ylabel('Customer Count', fontdict=small_font)
0121: ax_b.tick_params(axis='x', labelsize=15)
0122: ax_b.tick_params(axis='y', labelsize=13)
0123: ax_b.legend(loc='upper right', fontsize=13, frameon=False)
0124: ax_b.grid(axis='y', linestyle=':', alpha=0.12)
0125: ax_b.set_ylim(0, max(country_total) * 1.2)
0126: ax_note = fig.add_subplot(gs[2, 3:6])
0127: ax_note.set_facecolor(bg_color)
0128: for spine in ax_note.spines.values():
0129:     spine.set_edgecolor(border_color)
0130:     spine.set_linewidth(1.0)
0131: annotation_note = 'Churn tập trung tại nhóm khách hàng lớn tuổi, số dư cao, ít hoạt động.\nChiến lược:\n- Ưu tiên chăm sóc nhóm giá trị cao có dấu hiệu không active.\n- Đẩy mạnh onboarding cho nhóm mới/thụ động.\n- Theo dõi real-time, cảnh báo sớm.'
0132: ax_note.text(0.05, 0.98, 'Key Insights & Strategies:', fontdict=label_font, va='top')
0133: ax_note.text(0.05, 0.75, annotation_note, fontdict=small_font, va='top')
0134: ax_note.axis('off')
0135: save_fig(fig)