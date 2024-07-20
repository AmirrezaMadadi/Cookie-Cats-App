# Load dataset function
def load(path, info=True):

    import pandas as pd
    import numpy as np
    import io
    
    if len(path.split(".csv")) > 1:
        data = pd.read_csv(path)
    elif len(path.split(".xlsx")) > 1:
        data = pd.read_excel(path)

    if info:
        if len(data) > 0:
            print('# Data Imported!')
            print("# ------------------------------------", "\n")

            print("# Dimensions -------------------------")
            print("Observations:", data.shape[0], "Features:", data.shape[1], "\n")

            print("# dtypes -----------------------------")
            if len(data.select_dtypes("object").columns) > 0:
                print("Object Variables:", "\n", "# of Variables:", 
                      len(data.select_dtypes("object").columns), "\n", 
                      data.select_dtypes("object").columns.tolist(), "\n")
    
            if len(data.select_dtypes("integer").columns) > 0:
                print("Integer Variables:", "\n", "# of Variables:", 
                      len(data.select_dtypes("integer").columns), "\n", 
                      data.select_dtypes("integer").columns.tolist(), "\n")
    
            if len(data.select_dtypes("float").columns) > 0:
                print("Float Variables:", "\n", "# of Variables:", 
                      len(data.select_dtypes("float").columns), "\n", 
                      data.select_dtypes("float").columns.tolist(), "\n")
    
            if len(data.select_dtypes("bool").columns) > 0:
                print("Bool Variables:", "\n", "# of Variables:", 
                      len(data.select_dtypes("bool").columns), "\n", 
                      data.select_dtypes("bool").columns.tolist(), "\n")
    
            print("# Missing Values ---------------------")
            print("Are there any missing values? \n ", np.where(data.isnull().values.any() == False, 
                                                            "No missing value!", "Data includes missing value!"), "\n")
            
            buf = io.StringIO()
            data.info(buf=buf)
            info = buf.getvalue().split('\n')[-2].split(":")[1].strip()
            print("# Memory Usage ---------------------- \n", info)
          
        else:
            print("# Dataset did not import!")
    
    return data

# ========================================================================================================
# A / B testing function
def AB_testing(data, version, target, alpha):

    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    from scipy.stats import shapiro

    # Split A/B Versions
    group_A = data[data[version] == 'A'][target]
    group_B = data[data[version] == 'B'][target]

    # Assumption: Normality
    nt_A = shapiro(group_A)[1] < alpha
    nt_B = shapiro(group_B)[1] < alpha
    # H0: Distribution is Normal!
    # Ha: Distribution is not Normal!

    if (nt_A == False) and (nt_B == False): # H0: Normal Distribution

        # Parametric Test
        # Assumption: Homogeneity of variances
        leveneTest = (stats.levene(group_A, group_B)[1] / 2) < alpha
        # H0: Homogeneity: False
        # Ha: Heterogeneous: True

        if leveneTest == False:
            # Homogeneity
            ttest = stats.ttest_ind(group_A, group_B, equal_var=True)[1] / 2
            # H0: Ma == Mb - False
            # Ha: Ma < Mb - True
        else:
            # Heterogeneous
            ttest = stats.ttest_ind(group_A, group_B, equal_var=False)[1] / 2
            # H0: Ma == Mb - False
            # Ha: Ma < Mb - True
    else:
        # Non-Parametric Test
        ttest = stats.mannwhitneyu(group_A, group_B)[1] / 2
        # H0: Ma == Mb - False
        # Ha: Ma < Mb - True

    # Result
    temp = pd.DataFrame({
        'AB Hypothesis': [ttest < alpha],
        'p-value': [ttest]
    })

    temp['Test Type'] = np.where((nt_A == False) & (nt_B == False), 'Parametric', 'Non-Parametric')

    temp['AB Hypothesis'] = np.where(temp['AB Hypothesis'] == False, 'Fail to reject H0', 'Reject H0')

    temp['Comment'] = np.where(temp['AB Hypothesis'] == 'Fail to reject H0', 'A/B groups are similar!', 'A/B groups are not similar!')

    # Columns
    if (nt_A == False) and (nt_B == False):
        temp["Homogeneity"] = np.where(leveneTest == False, "Yes", "No")

        temp = temp[["Test Type", "Homogeneity","AB Hypothesis", "p-value", "Comment"]]
    else:
        temp = temp[["Test Type","AB Hypothesis", "p-value", "Comment"]]

    # Print Hypothesis
    print("# A/B Testing Hypothesis")
    print("H0: A == B")
    print("Ha: A != B")

    return temp
