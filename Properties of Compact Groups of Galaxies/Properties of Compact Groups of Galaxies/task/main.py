# write yor code here
import pandas as pd
import scipy
import matplotlib.pyplot as plt
from astropy.cosmology import FlatLambdaCDM
from astropy import units as u
from astropy.coordinates import SkyCoord
import itertools

# To complete this stage:
# 1.Read the following dataset: groups.tsv. TSV stands for tab-separated values.
df = pd.read_csv('..\\groups.tsv', delimiter="\t")

# 2. Remove the missing values from the dataset, you can use the dropna function;
df.dropna(inplace=True)

# 3. Find a mean value for the IGL mean surface brightness in groups of galaxies with LSB features and without them;
mean_IGL = df.groupby('features').agg({'mean_mu': 'mean'})

# 4. Print two floating-point numbers     
    # (the mean value of the mean surface brightness for galaxies with LSB features and without them) split with a space.
#print(mean_IGL.mean_mu[1], mean_IGL.mean_mu[0], sep=' ')



# In this stage, perform the following analysis:
# 1. Conduct the Shapiro-Wilk Normality test for the IGL mean surface brightness (the mean_mu column) in
    # galaxies with LSB features and without them.
df1 = df[(df.features == 1)]
df2 = df[(df.features == 0)]
Shapiro_Wilk1 = scipy.stats.shapiro(df1['mean_mu'])
Shapiro_Wilk2 = scipy.stats.shapiro(df2['mean_mu'])

# 2. Perform the Fligner-Killeen Homogeneity test for variances of the same two data samples.
    # This is to check condition #3: the samples came from populations with equal variances.
Fligner_Killeen = scipy.stats.fligner(df1['mean_mu'], df2['mean_mu'])

# 3. Perform the one-way ANOVA test and obtain a p-value.
ANOVA = scipy.stats.f_oneway(df1['mean_mu'], df2['mean_mu'])

# 4. Print four floating-point numbers. Separate them with one space:
    # two p-values for the Shapiro-Wilk test for galaxies with LSB features and without them,
    # one p-value obtained from the Fligner-Killeen test,
    # and one p-value of the ANOVA test.
#print(Shapiro_Wilk1[1], Shapiro_Wilk2[1], Fligner_Killeen[1], ANOVA[1], sep=' ')



#1. Read the datasets: galaxies_morphology.tsv and isolated_galaxies.tsv;
galaxies_morphology = pd.read_csv('..\\galaxies_morphology.tsv', delimiter="\t")
isolated_galaxies = pd.read_csv('..\\isolated_galaxies.tsv', delimiter="\t")

#2. Plot the histograms for the Sérsic index for both datasets;
names = ["groups galaxies", "isolated galaxies"]
plt.hist([galaxies_morphology['n'], isolated_galaxies['n']], stacked=True, label=names)
plt.ylabel("Count")
plt.xlabel("n")
plt.legend()
plt.show()

#3. Calculate a fraction of galaxies with the Sérsic index >2n>2 for both datasets;
groupGalaxiesFraction = galaxies_morphology[(galaxies_morphology['n'] > 2)].n.count() / galaxies_morphology['n'].count()
isolatedGalaxiesFraction = isolated_galaxies[(isolated_galaxies['n'] > 2)].n.count() / isolated_galaxies['n'].count()

#4. Perform the two-sample Kolmogorov-Smirnov test for equality for datasets and obtain a p-value.
    #Note that you must use a two-sided alternative for this test. It means that the null hypothesis is
    #that the two given samples are drawn from the same probability distribution;
Kolmogorov_Smirnov_test = scipy.stats.ks_2samp(galaxies_morphology['n'], isolated_galaxies['n'])

#5. Print three floating-point numbers separated by one space:
    # fractions of galaxies with the Sersic index >2n>2 for groups' galaxies and isolated galaxies,
    # and a p-value obtained from the Kolmogorov-Smirnov test.
#print(groupGalaxiesFraction, isolatedGalaxiesFraction, Kolmogorov_Smirnov_test[1], sep=' ')



#1. Continue working with galaxies_morphology.tsv from the previous stage. Group data by the Group column.
    #The values of the new table will be the mean Sérsic index (n) and the mean numerical galaxy type (T).
    #Create the columns mean_n and mean_T for obtained values with the help of the agg function from pandas.
gr_galaxies_morphology = galaxies_morphology.groupby(['Group']).mean()
gr_galaxies_morphology.rename(columns={'n': 'mean_n', 'T': 'mean_T'}, inplace=True)

#2. Use the Group column and merge the data table with the one from groups.tsv that you preprocessed in Stage 1;
merged_df = pd.merge(df, gr_galaxies_morphology, how='left', left_on='Group', right_on='Group')
merged_df.dropna(inplace=True)

#3. Plot scatterplots for the following value-pairs:
    #mean_mu-mean_n
    #mean_mu-mean_T;
#plt.scatter(merged_df['mean_n'], merged_df['mean_mu'], c='red', s=30)
#plt.gca().invert_yaxis()
#plt.xlabel("n")
#plt.ylabel("mu")
#plt.show()
#plt.scatter(merged_df['mean_T'], merged_df['mean_mu'], c='red')
#plt.gca().invert_yaxis()
#plt.xlabel("T")
#plt.ylabel("mu")
#plt.show()

#4. Conduct the Shapiro-Wilk Normality test for three variables: mean_mu, mean_n, and mean_T;
Shapiro_Wilk_mean_mu = scipy.stats.shapiro(merged_df['mean_mu'])
Shapiro_Wilk_mean_n = scipy.stats.shapiro(merged_df['mean_n'])
Shapiro_Wilk_mean_T = scipy.stats.shapiro(merged_df['mean_T'])

#5. Calculate the Pearson correlation coefficients and the corresponding p-values for testing non-correlation.
    #The null hypothesis of the test is that the considered populations are not correlated;
pearson_correlation_mean_n = scipy.stats.pearsonr(merged_df['mean_mu'], merged_df['mean_n'])
pearson_correlation_mean_T = scipy.stats.pearsonr(merged_df['mean_mu'], merged_df['mean_T'])

#6. Print five floating-point numbers separated by one space:
    #p-values for normality testing of
        #mean_mu,
        #mean_n
        #and mean_T,
    #and p-values for testing non-correlation for
        #mean_mu-mean_n
        #and mean_mu-mean_T.
#print(Shapiro_Wilk_mean_mu[1],
      #Shapiro_Wilk_mean_n[1],
      #Shapiro_Wilk_mean_T[1],
      #pearson_correlation_mean_n[1],
      #pearson_correlation_mean_T[1],
      #sep=' ')


# 1. Initialize the ΛCDM cosmology model with the parameters
cosmo = FlatLambdaCDM(H0=67.74, Om0=0.3089)

# 2. Read the dataset with galaxies' equatorial coordinates:
gm = pd.read_csv('..\\galaxies_morphology.tsv', delimiter='\t')
gm.dropna(axis=0, inplace=True)
ig = pd.read_csv('..\\isolated_galaxies.tsv', delimiter='\t')
ig.dropna(axis=0, inplace=True)
gr = pd.read_csv('..\\groups.tsv', delimiter='\t')
gr.dropna(axis=0, inplace=True)
gc = pd.read_csv('..\\galaxies_coordinates.tsv', delimiter='\t')
gc.dropna(axis=0, inplace=True)

# 3. Calculate the angular diameter distances, dA, in kiloparsecs for groups' median redshifts (the z column in groups.tsv)
# using the cosmology model method angular_diameter_distance.
da = list(map(lambda z: cosmo.angular_diameter_distance(z).to(u.kpc), gr['z']))

# 4. Calculate the projected median separation.
# It is the median of the pairwise projected distance between the galaxies in each group. Denoted as r in the formula.
d1 = gr['z'].to_numpy()
dd = gr['z'].to_numpy()
mu = gr['mean_mu'].to_numpy()

def pp(ra1, dec1, ra2, dec2):
    p1 = SkyCoord(ra=ra1 * u.degree, dec=dec1 * u.degree, frame="fk5")
    p2 = SkyCoord(ra=ra2 * u.degree, dec=dec2 * u.degree, frame="fk5")
    return p1.separation(p2)

i_group = 0
for group in gr['Group']:
    ggc = gc[gc.Group == group]

    ddd = []
    for item in itertools.combinations(ggc[['RA', 'DEC']].to_numpy(), 2):
        p1p2 = pp(item[0][0], item[0][1], item[1][0], item[1][1])
        d1d2 = p1p2.to(u.rad) * da[i_group]
        d1d2 = d1d2.value
        ddd.append(d1d2)

    m = pd.DataFrame(ddd, columns=['median']).median()['median']
    dd[i_group] = m

    i_group += 1

# 5. Plot a scatterplot for the projected median separation and the IGL mean surface brightness;
plt.title("scattering diagram")
plt.xlabel("R (kpc)")
plt.ylabel("mu (IGL)")
plt.scatter(dd, mu, s=100)
plt.gca().invert_yaxis()
plt.show()

# 6. Conduct the Shapiro-Wilk Normality test for the projected median separation and mean_mu;
p1 = scipy.stats.shapiro(dd)[1]
p2 = scipy.stats.shapiro(mu)[1]

# 7. Calculate the Pearson correlation coefficient and the corresponding p-value
    # for testing the non-correlation for these values;
p3 = scipy.stats.pearsonr(dd, mu)[1]

# 8. Print four floating-point numbers separated with one space:
    # the median separation for the HCG 2 group,
    # p-values for the normality test of the projected median separation
    # and mean_mu,
    # and a p-value for testing the non-correlation for these values.
print(dd[0], p1, p2, p3)