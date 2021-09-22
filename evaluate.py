import pandas as pd
import numpy as np
import scipy.stats as stats


def get_t_test(t_var, df, var1, target, alpha=0.05, tail_type = 2, var=False , var2=None):
    '''
        This method will produce a 1 or 2 tailed t test to equate the p value to the alpha to determine whether the null hypothesis can be rejected.
        tail
    ''' 
    for i in t_var:
        stat, p = stats.levene(df[i], df[target])
        if p > alpha:
            var = True
        if tail_type == 1:
            a = df.loc[df[target] == var1, i].to_numpy()
            t, p = stats.ttest_1samp(a, df[target].mean())
            print('Null Hypothesis: for {}, the {} mean when {} == {} is the same as the population mean'.format(i, target, target, var1))
            print('Alternative hypothesis: for {}, the {} mean when {} == {} is not the same as the population mean'.format(i, target, target, var1))
            if p/2 < alpha:
                print('p value {} is less than alpha {} , we reject our null hypothesis'.format(p,alpha))
            else:
                print('p value {} is not less than alpha {} , we  fail to reject our null hypothesis'.format(p,alpha))
            print('-----------------------------------')

            
        elif tail_type == 2:
            a = df.loc[df[target] == var1, i].to_numpy()
            b = df.loc[df[target] == var2, i].to_numpy()
            t, p = stats.ttest_ind(a,b, equal_var=var)
       
            print('Null Hypothesis: the mean value of {} is the same when {} == {} and {}'.format(i, target, var1, var2))
            print('Alternative hypothesis: the mean value of {} is not the same when {} == {} and {}')
            if p < alpha:
                print('p value {} is less than alpha {} , we reject our null hypothesis'.format(p,alpha))
            else:
                print('p value {} is not less than alpha {} , we  fail to reject our null hypothesis'.format(p,alpha))
            print('-----------------------------------')

def get_pearsons(con_var, target, alpha, df):
     for i in con_var:
        t, p = stats.pearsonr(df[i],df[target])
        print('Null Hypothesis: {} is independent to {} '.format(i, target))
        print('Alternative hypothesis:  {} is not independent to {} '.format(i, target))
        if p < alpha:
            print('p value {} is less than alpha {} , we reject our null hypothesis'.format(p,alpha))
        else:
            print('p value {} is not less than alpha {} , we  fail to reject our null hypothesis'.format(p,alpha))
        print('------------------------------------')
        

def get_spearmanr(con_var, target, alpha, df):
    for i in con_var:
        t,p = stats.spearman(df[i], df[target])
        print('Null Hypothesis: {} is independent to {} '.format(i, target))
        print('Alternative hypothesis:  {} is not independent to {} '.format(i, target))
        if p < alpha:
            print('p value {} is less than alpha {} , we reject our null hypothesis'.format(p,alpha))
        else:
            print('p value {} is not less than alpha {} , we  fail to reject our null hypothesis'.format(p,alpha))
        print('-------------------------------------')
        
        


def get_chi_test(chi_list, df, alpha):
    '''
    This method will produce a chi-test contengency, and equate the p value to the alpha to determine whether the null hypothesis can be rejected.
    '''
    
    for i in chi_list:
        observed = pd.crosstab(df[i], df.churn)
        print(observed)
        chi2, p, degf, expected = stats.chi2_contingency(observed)
        print('Null Hypothesis: {} is independent to {} '.format(i, target))
        print('Alternative hypothesis:  {} is not independent to {} '.format(i, target))
        if p < alpha:
            print('p value {} is less than alpha {} , we reject our null hypothesis'.format(p,alpha))
        else:
            print('p value {} is not less than alpha {} , we  fail to reject our null hypothesis'.format(p,alpha))
        print('--------------------------------------')
        