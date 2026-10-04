import seaborn as sns
import matplotlib.pyplot as plt


# Visualize the distribution with KDE
sns.kdeplot(data=df, x='Re_kpc', fill=True)
plt.title('KDE of Galaxy Effective Radius')
plt.show()


# Create 20 quantile-based bins based on the distribution
df['z_bin'] = pd.qcut(df, q=20, labels=False, duplicates='drop')
