0001: import matplotlib
0002: from matplotlib import pyplot as plt
0003: from matplotlib.gridspec import GridSpec
0004: from matplotlib.patches import Rectangle, Wedge
0005: from matplotlib.ticker import MaxNLocator
0006: needed_cols = ['churn', 'age', 'balance', 'products_number', 'active_member', 'gender', 'country', 'estimated_salary']
0007: col_available = lambda col: col in df.columns
0008: palette = ['#3498db', '#e67e22', '#e74c3c', '#2ecc71', '#9b59b6']
0009: kpi_card_color = ['#2ecc71', '#3498db', '#e67e22', '#e74c3c']
0010: card_bg = '#fcfcfc'
0011: border_c = '#d0d0d0'
0012: fig = plt.figure(figsize=(19.2, 10.8), constrained_layout=False)
0013: grid = GridSpec(3, 6, figure=fig, wspace=0.15, hspace=0.22)
0014: kpi_labels = ['Churn Rate (%)', 'Retention Rate (%)', 'Cross-sell Rate (%)', 'Active Member Rate (%)']
0015: kpi_values = []
0016: sparkline_data = []
0017: kpi_status_text = []
0018: if col_available('churn'):
0019:     churn_val = np.round(100 * df['churn'].mean(), 2)
0020:     kpi_values.append(churn_val)
0021:     churn_spark = df['churn'].rolling(window=200).mean().values
0022:     sparkline_data.append(churn_spark)
0023:     if churn_val < 15:
0024:         kpi_status_text.append('Promoters')
0025:     elif churn_val < 25:
0026:         kpi_status_text.append('Passives')
0027:     else:
0028:         kpi_status_text.append('Detractors')
0029: else:
0030:     kpi_values.append(None)
0031:     sparkline_data.append(None)
0032:     kpi_status_text.append('N/A')
0033: if col_available('churn'):
0034:     retention_val = np.round(100 * (1 - df['churn'].mean()), 2)
0035:     kpi_values.append(retention_val)
0036:     retention_spark = 1 - df['churn'].rolling(window=200).mean().values
0037:     sparkline_data.append(retention_spark)
0038:     if retention_val > 85:
0039:         kpi_status_text.append('Promoters')
0040:     elif retention_val > 75:
0041:         kpi_status_text.append('Passives')
0042:     else:
0043:         kpi_status_text.append('Detractors')
0044: else:
0045:     kpi_values.append(None)
0046:     sparkline_data.append(None)
0047:     kpi_status_text.append('N/A')
0048: if col_available('products_number'):
0049:     cross_sell_val = np.round(100 * (df['products_number'] > 2).mean(), 2)
0050:     cross_sell_spark = (df['products_number'].rolling(window=200).mean() > 2).astype(float).values
0051:     kpi_values.append(cross_sell_val)
0052:     sparkline_data.append(cross_sell_spark)
0053:     if cross_sell_val > 10:
0054:         kpi_status_text.append('Promoters')
0055:     elif cross_sell_val > 5:
0056:         kpi_status_text.append('Passives')
0057:     else:
0058:         kpi_status_text.append('Detractors')
0059: else:
0060:     kpi_values.append(None)
0061:     sparkline_data.append(None)
0062:     kpi_status_text.append('N/A')
0063: if col_available('active_member'):
0064:     active_member_val = np.round(100 * df['active_member'].mean(), 2)
0065:     active_member_spark = df['active_member'].rolling(window=200).mean().values * 100
0066:     kpi_values.append(active_member_val)
0067:     sparkline_data.append(active_member_spark)
0068:     if active_member_val > 60:
0069:         kpi_status_text.append('Promoters')
0070:     elif active_member_val > 40:
0071:         kpi_status_text.append('Passives')
0072:     else:
0073:         kpi_status_text.append('Detractors')
0074: else:
0075:     kpi_values.append(None)
0076:     sparkline_data.append(None)
0077:     kpi_status_text.append('N/A')
0078: for i in range(4):
0079:     ax = fig.add_subplot(grid[0, i])
0080:     ax.add_patch(Rectangle([0, 0], 1, 1, facecolor=card_bg, edgecolor=border_c, linewidth=1))
0081:     ax.axis('off')
0082:     if kpi_values[i] is None:
0083:         ax.text(0.5, 0.65, 'No data', color='#888', fontsize=23, fontweight='bold', ha='center', va='center')
0084:         ax.text(0.5, 0.48, kpi_labels[i], fontsize=16, ha='center', color='#666')
0085:         continue
0086:     ax.text(0.5, 0.68, f'{kpi_values[i]:.2f}%', color=kpi_card_color[i], fontsize=44, fontweight='bold', ha='center', va='center')
0087:     ax.text(0.5, 0.47, kpi_labels[i], fontsize=19, ha='center', color='#444')
0088:     ax.text(0.5, 0.32, kpi_status_text[i], fontsize=13, color='#888', ha='center')
0089:     if sparkline_data[i] is not None and len(sparkline_data[i]) > 10:
0090:         line_x = np.arange(len(sparkline_data[i]))
0091:         mini_x = line_x[-30:] if len(line_x) > 30 else line_x
0092:         mini_y = sparkline_data[i][-30:] if len(sparkline_data[i]) > 30 else sparkline_data[i]
0093:         ax.plot(mini_x / mini_x.max(), mini_y / np.max(mini_y), lw=1.8, color=kpi_card_color[i], clip_on=False, transform=ax.transAxes)
0094:         ax.set_xlim(0, 1)
0095:         ax.set_ylim(0, 1)
0096: ax_gender = fig.add_subplot(grid[1, 0:2])
0097: ax_gender.set_facecolor(card_bg)
0098: for spine in ax_gender.spines.values():
0099:     spine.set_edgecolor(border_c)
0100:     spine.set_linewidth(1)
0101: ax_gender.axis('equal')
0102: if col_available('churn') and col_available('gender'):
0103:     gender_labels = df['gender'].unique()
0104:     if len(gender_labels) == 2:
0105:         gender_churn = [df[df['gender'] == g]['churn'].mean() for g in gender_labels]
0106:         sizes = [g * 100 for g in gender_churn]
0107:         colors = palette[:2] if len(gender_labels) >= 2 else palette
0108:         (wedges, texts) = ax_gender.pie(sizes, labels=[f'{g}\n{np.round(s, 2)}%' for (g, s) in zip(gender_labels, sizes)], colors=colors, startangle=130, autopct='%1.1f%%', wedgeprops={'linewidth': 1, 'edgecolor': border_c})
0109:         ax_gender.set_title('Churn Rate theo Giới', fontsize=19, fontweight='semibold', color='#555')
0110:     else:
0111:         ax_gender.text(0.5, 0.5, 'Insufficient Gender Data', ha='center', va='center', fontsize=17, color='#999')
0112: else:
0113:     ax_gender.text(0.5, 0.5, 'No Gender/Churn Data', ha='center', va='center', fontsize=17, color='#999')
0114: ax_country = fig.add_subplot(grid[1, 2:4])
0115: ax_country.set_facecolor(card_bg)
0116: for spine in ax_country.spines.values():
0117:     spine.set_edgecolor(border_c)
0118:     spine.set_linewidth(1)
0119: ax_country.axis('equal')
0120: if col_available('churn') and col_available('country'):
0121:     country_labels = df['country'].unique()
0122:     churn_by_country = [df[df['country'] == c]['churn'].mean() for c in country_labels]
0123:     sizes = [100 * x for x in churn_by_country]
0124:     colors = palette[:len(country_labels)]
0125:     (wedges, texts) = ax_country.pie(sizes, labels=[f'{c}\n{np.round(s, 2)}%' for (c, s) in zip(country_labels, sizes)], colors=colors, startangle=170, wedgeprops={'linewidth': 1, 'edgecolor': border_c})
0126:     ax_country.set_title('Churn Rate theo Quốc gia', fontsize=19, fontweight='semibold', color='#555')
0127: else:
0128:     ax_country.text(0.5, 0.5, 'No Country/Churn Data', ha='center', va='center', fontsize=17, color='#999')
0129: ax_line = fig.add_subplot(grid[1, 4:6])
0130: ax_line.set_facecolor(card_bg)
0131: for spine in ax_line.spines.values():
0132:     spine.set_edgecolor(border_c)
0133:     spine.set_linewidth(1)
0134: if col_available('age') and col_available('churn'):
0135:     bins = np.arange(df['age'].min(), df['age'].max() + 5, 5)
0136:     churn_by_age = df.groupby(np.digitize(df['age'], bins))['churn'].mean() * 100
0137:     tick_labels = [f'{int(bins[i])}-{int(bins[i + 1] - 1)}' for i in range(len(bins) - 1)]
0138:     ax_line.plot(tick_labels, churn_by_age.values, color=palette[0], marker='o', lw=2)
0139:     ax_line.set_title('Churn theo Độ tuổi', fontsize=19, fontweight='semibold', color='#555')
0140:     ax_line.set_xlabel('Nhóm tuổi', fontsize=13)
0141:     ax_line.set_ylabel('Churn Rate (%)', fontsize=13)
0142:     max_idx = np.argmax(churn_by_age.values)
0143:     ax_line.annotate(f'{churn_by_age.values[max_idx]:.1f}%', xy=(max_idx, churn_by_age.values[max_idx]), xytext=(max_idx, churn_by_age.values[max_idx] + 6), arrowprops=dict(arrowstyle='->', color=palette[2], lw=1), color=palette[2], fontsize=12)
0144:     ax_line.grid(alpha=0.13)
0145: else:
0146:     ax_line.text(0.5, 0.5, 'No Age/Churn Data', ha='center', va='center', fontsize=17, color='#999')
0147: ax_bar = fig.add_subplot(grid[2, 0:3])
0148: ax_bar.set_facecolor(card_bg)
0149: for spine in ax_bar.spines.values():
0150:     spine.set_edgecolor(border_c)
0151:     spine.set_linewidth(1)
0152: if col_available('balance') and col_available('churn'):
0153:     bins = [0, 1, 51002, 100194, 149388, df['balance'].max() + 1]
0154:     labels = ['Zero', 'Low', 'Med', 'High', 'Very High']
0155:     categories = np.digitize(df['balance'], bins)
0156:     churn_rate_by_bal = [df[categories == i]['churn'].mean() * 100 for i in range(1, 6)]
0157:     total_count_by_bal = [np.sum(categories == i) for i in range(1, 6)]
0158:     ax_bar.bar(labels, churn_rate_by_bal, color=palette[3], alpha=0.8, edgecolor=border_c, linewidth=1)
0159:     ax_bar.set_ylabel('Churn Rate (%)', fontsize=13)
0160:     ax_bar.set_xlabel('Nhóm Số dư', fontsize=13)
0161:     ax_bar.set_title('Churn theo Số dư tài khoản', fontsize=19, fontweight='semibold', color='#555')
0162:     ax_bar.grid(axis='y', alpha=0.18)
0163:     max_idx = np.argmax(churn_rate_by_bal)
0164:     ax_bar.annotate(f'{churn_rate_by_bal[max_idx]:.1f}%', xy=(max_idx, churn_rate_by_bal[max_idx]), xytext=(max_idx + 0.1, churn_rate_by_bal[max_idx] + 3), color='#e74c3c', fontsize=13, arrowprops=dict(arrowstyle='->', color=palette[2], lw=1))
0165: else:
0166:     ax_bar.text(0.5, 0.5, 'No Balance/Churn Data', ha='center', va='center', fontsize=17, color='#999')
0167: ax_note = fig.add_subplot(grid[2, 3:6])
0168: ax_note.set_facecolor(card_bg)
0169: for spine in ax_note.spines.values():
0170:     spine.set_edgecolor(border_c)
0171:     spine.set_linewidth(1)
0172: ax_note.axis('off')
0173: if col_available('country') and col_available('churn'):
0174:     countries = df['country'].unique()
0175:     churn_table = [[c, f"{100 * df[df['country'] == c]['churn'].mean():.2f}%"] for c in countries]
0176:     table = ax_note.table(cellText=churn_table, colLabels=['Quốc gia', 'Churn Rate'], cellLoc='center', loc='center')
0177:     table.auto_set_font_size(False)
0178:     table.set_fontsize(13)
0179:     table.scale(1, 1.3)
0180:     ax_note.set_title('Bảng Churn Rate theo Quốc gia', fontsize=17, color='#555')
0181: else:
0182:     placeholder_note = '📌 Ghi chú tổng quan:\n\nKhông đủ dữ liệu cho bảng churn phân theo quốc gia.\n- Nếu có dữ liệu đầy đủ, bảng sẽ hiển thị nhanh các churn rate từng quốc gia.\n- Ưu tiên kiểm soát churn tại nhóm khách hàng giá trị cao và quốc gia số lượng lớn.'
0183:     ax_note.text(0.05, 0.98, placeholder_note, fontsize=15, color='#888', ha='left', va='top')
0184: fig.suptitle('Dashboard Tổng hợp Phân tích Churn Khách hàng Ngân hàng', fontsize=26, fontweight='bold', color='#242424', y=0.98)
0185: save_fig(fig)