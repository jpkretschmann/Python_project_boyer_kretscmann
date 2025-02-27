"""
Created on Sun Nov 27 10:45:39 2022
@author: gaspb jpk
"""


import streamlit as st
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import matplotlib.pyplot as plt 
import seaborn as sns
import statsmodels.formula.api as smf
import statsmodels.api as sm
import scipy.stats as si


from sklearn import preprocessing
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor 
from sklearn.model_selection import cross_val_score, train_test_split, KFold, GridSearchCV, StratifiedKFold, train_test_split 
from sklearn.metrics import confusion_matrix, accuracy_score, mean_squared_error, classification_report, roc_auc_score, roc_curve

plt.rc("font", size=14)


url = "https://raw.githubusercontent.com/jpkretschmann/Python_project_boyer_kretscmann/main/heart_failure.csv"
df = pd.read_csv(url, sep=',')
df = df.rename(columns = {'age':'Age',
                          'anaemia':'Anaemia',
                          'creatinine_phosphokinase':'CPK',
                          'diabetes':'Diabetes',
                          'ejection_fraction':'Ejection fraction',
                          'high_blood_pressure':'High blood pressure',
                          'platelets':'Level of platelets',
                          'serum_creatinine':'Level of creatinine',
                          'serum_sodium':'Level of sodium',
                          'sex':'Sex',
                          'smoking':'Smoking',
                          'time':'Number of day survied post diagnostic',
                          'DEATH_EVENT':'Dead'})




# Creating more handy dataframe
alive_df = df[df['Dead'] == 0]
dead_df = df[df['Dead'] == 1]
men_df = df[df['Sex'] == 0]
women_df = df[df['Sex'] == 1]

st.title('Heart Failure Problem')

st.header('Introduction and descriptive statistic')
st.subheader('What is a heart failure ?')
st.write('Heart failure is the inability of the heart muscle to normally propel blood through the body. It is a frequent and potentially severe disease, with a strong impact on the quality of life if it is not detected in time and treated. It can occur, for example, in the course of a myocardial infarction or angina pectoris.') 

st.write('Heart failure occurs when the heart loses some of its muscular strength and normal contraction capacity; it no longer pumps enough blood to allow the organs to receive enough oxygen and nutrients, which are essential for their proper functioning.')

st.write('Initially, the heart tries to adapt to the loss of its contraction force by accelerating its beats (increase in heart rate), then it increases in volume (thickening of the walls or dilation of the cardiac chambers). This extra workload for the heart eventually leads to heart failure.')

# Creation of some of the statistics
men_survival_rate = round(len(men_df[men_df['Dead']==0].index)/len(men_df.index)*100)
women_survival_rate =  round(len(women_df[women_df['Dead']==0].index)/len(women_df.index)*100)
median_survival_day_men = men_df[men_df['Dead']==0]['Number of day survied post diagnostic'].median()
median_survival_day_women = women_df[women_df['Dead']==0]['Number of day survied post diagnostic'].median()

st.write('In 2001 in France, the number of people with heart failure was 500,000, with 120,000 new cases each year.  Heart failure is responsible for more than 32,000 deaths per year. Properly managed, this disease does not lead directly to death. Indeed, on a sample of about 300 people, we estimate a survival rate of survival for both men and woman of', men_survival_rate,'%. Moreover, we note that for the deceased, the median number of days of survival after diagnosis is', median_survival_day_men, 'days for men and for women ', median_survival_day_women, ' days.' )
st.write('In this application we are describing the different physiological measurements and indicators medically realted to the occurence of heart disease. Hereby we investigate patients who endure heart disease and try to explain which variables could indicate a possible heart faulure, thus death, in the future due to the heart disease.')

st.subheader('What are the indicators ?')
st.write('Thus, it is essential to detect it as soon as possible.' 
'To do this, doctors and other health specialists base their work on a number of physiological measurements. Among these we count : ')

physiological_measurements = st.selectbox(
    'Wish physiological measurements would you like to investigate ? ',
    ('CPK','Ejection fraction','Level of platelets', 'Level of creatinine', 'Level of sodium'),   
    )

distribution_physiological_measurements = px.histogram(df, physiological_measurements, color='Sex', barmode='group', histnorm ='percent', title= 'Distribution of '+physiological_measurements+' among the patients grouped by sex')
distribution_physiological_measurements3 = px.box(df, x= 'Dead', y= physiological_measurements, color ='Sex', title= 'Comparison of '+physiological_measurements+' among the dead and alive patients')



st.plotly_chart(distribution_physiological_measurements)
st.plotly_chart(distribution_physiological_measurements3)


with st.expander('Interested in a more detailed explanation ?'):
    if (physiological_measurements=='CPK'):
        st.write(' CPK or Creatine PhosphoKinase is an important protein in energy metabolism.'
                 ' Its role is to replenish ATP (adenosine triphosphate) reserves, which can be used by the cell for its respiration and energy. Its determination is of interest in the diagnosis of myocardial infarction (increase in the MB fraction), muscle damage (increase in the MM fraction) and meningeal damage.')
        st.write('Its normal rate is for men: 0 - 195 IU/l and women: 0 - 170 IU/l, the main origins of an elevation of CPK are an attack of the cardiac muscle, skeletal muscles, meninges...etc')
        st.write('We can see from the distribution that people with heart failure tend to have a CPK above the recommended level. Note that the median for men is', men_df['CPK'].median(),' IU/l and the median for women is',women_df['CPK'].median(),' IU/l.')
    elif (physiological_measurements=='Ejection fraction'):
        st.write('The ejection fraction (EF) is the percentage of blood ejection from a heart chamber during a beat. '
                 ' When the ejection fraction is decreased, the body can maintain cardiac output in two ways: by increasing the heart rate, or by maintaining a constant systolic ejection volume by increasing the end-diastolic volume of the ventricle. ')
        st.write('Increasing the end-diastolic volume results in dilation of the ventricle and thus the heart. This stretching of the cardiac muscle fibers, due to the elastic properties of the muscle fibers, allows a transient improvement of its contraction and is therefore an adaptation mechanism, often deleterious in the long term (Frank-Starling law).')
        st.write('When these compensation mechanisms are exceeded, cardiac output decreases and becomes insufficient for the body needs. A picture of cardiac insufficiency sets in.')
        st.write('It is of the order of 50 to 70% in the normal individual (typical normal value: 60%), and may be decreased in case of abnormal contractility, and may go down to 10-15% in case of major dysfunction, often responsible for heart failure. In case of heart failure, its value allows to distinguish between systolic (low ejection fraction) and diastolic heart failure (called "preserved systolic function").')        
        st.write('Here also the analysis of the distribution of this indicator shows us that people with heart failure have an insufficient level on average. The median for men is', men_df['Ejection fraction'].median(),' % and for women',women_df['Ejection fraction'].median(),' %. This result seems to us consistent when we put in perspective the previous explanations and causes of heart failure.')
    elif (physiological_measurements=='Level of platelets'):
        st.write('Platelets (or thrombocytes) are lenticular, biconvex disc-shaped, and measure between 1.5 and 3.5 µm in diameter. Their main function is to stop bleeding quickly. Their normal concentration is 150,000 to 400,000 /µL of blood. ')
        st.write('When the concentration is less than 150,000/µL, it is called thrombocytopenia. This thrombocytopenia can result in emorargy related to a coagulation defect.')
        st.write('When it is higher than 400 000 /µL, it is called thrombocytosis. This can lead to venous trombosis: a blood clot due to an excess of coagulation that can lead to strokes.')
        st.write('In view of the distribution, we notice that people with heart failure are in the average. This indicator does not seem to be the most relevant to identify a heart failure. ')
    elif (physiological_measurements=='Level of creatinine'):
        st.write('Creatinine is a chemical compound left over from the energy production processes in your muscles. Healthy kidneys filter creatinine from the blood. Creatinine leaves your body as a waste product in the urine.')
        st.write('Creatinine usually enters your bloodstream and is filtered out of the bloodstream at a generally constant rate. The amount of creatinine in your blood should be relatively stable. An increase in creatinine levels may be a sign of poor kidney function.')
        st.write('Serum creatinine is expressed in milligrams of creatinine per deciliter of blood (mg/dL) or micromoles of creatinine per liter of blood (micromoles/L). The typical range for serum creatinine is: For adult men, 0.74 to 1.35 mg/dL (65.4 to 119.3 micromoles/L). For adult women, 0.59 to 1.04 mg/dL (52.2 to 91.9 micromoles/L).')
        st.write('While the male distribution appears to be normal, the female distribution is above normal. The median is recorded at ', women_df['Level of creatinine'].median(),' mg/dL. This seems to indicate that women seem to develop kidney and heart failure at the same time. This phenomenon is documented in medicine and seems to be due to nutritional problems resulting in a degradation of these two organs. ')
    else :
        st.write('This test determines the amount of sodium in your blood. Sodium is particularly important for nerve and muscle function. Your body maintains sodium balance through various mechanisms. Sodium enters your bloodstream through food and drink. It leaves the bloodstream through urine, stool and sweat. Having the right amount of sodium is important for your health. Too much sodium can increase your blood pressure.The regulation of sodium in the body is ensured by the renal functions.')
        st.write('Normal results for this test are 135 to 145 mEq/L (milliequivalents per liter), according to the Mayo Clinic. But different labs use different values for "normal". A blood sodium level below 135 mEq/L is called hyponatremia. Hypernatremia means high levels of sodium in the blood. It is defined as levels that exceed 145 mEq/L.')
        st.write('Although the distribution of sodium level is wide, the level of our patients is concentrated around normal values. For men and woman both median are at ', women_df['Level of sodium'].median(),' mEq/L. This test is more recommended to evaluate the renal capacities of the patient, than cardiac.')





#############


st.subheader('The different causes')

st.write('As already stated, heart failure is the inability of the heart to pump blood through the rest of the body. Remember that heart disease is just the diminished ability of the heart to pump blood through the system efficiently.')

st.write('This abnormality can be caused by a number of causes.  In this part we try to detail them. ')

cause = st.selectbox(
    'Wish causes would you like to investigate ? ',
    ('Age','Anaemia','Diabetes', 'High blood pressure', 'Smoking')
    )

if cause == 'Age':
  cause_distribution = px.histogram(df,x=cause, color='Dead',barmode='group', title = 'Distribution of the morbidity in function of '+cause)
  st.plotly_chart(cause_distribution)
else:
  cause_distribution = px.histogram(df, cause, color ='Sex', barmode='group', histnorm = 'percent', title= 'Density of '+cause+' among the patients', text_auto = True)
  cause_distribution.update_xaxes(type='category')
  cause_distribution3 = px.histogram(df, x='Age', y= cause , histnorm = 'density', title= 'Distribution of '+cause+' disease among age groups')
  
  st.plotly_chart(cause_distribution)
  st.plotly_chart(cause_distribution3)  


with st.expander('Interested in a more detailed explanation ?'):
        if (cause=='Age'):
            st.write('With age, the body tends to deteriorate. This decrepitude extends in particular to the cardiac muscle which tends to weaken. And thus to be less able to fulfill its functions.')
            st.write('Even if, it is the incentive greatly. The age does not automatically imply a cardiac insufficiency. Thus, it cannot be associated with a particular type of heart failure.')
            st.write("Furthermore, in the case that not all information about the patient's pathologies is detected, age can be used as a way to approximate them.")
        elif (cause=='Anaemia'):
            st.write('Anaemia (Iron deficiency) is a condition in which the number of red blood cells or the haemoglobin concentration within them is lower than normal. Haemoglobin is needed to carry oxygen and if you have too few or abnormal red blood cells, or not enough haemoglobin, there will be a decreased capacity of the blood to carry oxygen to the body’s tissues. In more severe anemia, the body may compensate for the lack of oxygen-carrying capability of the blood by increasing cardiac output (incresing the heart rate). However, this makes it easier for the body to reach its limits. The person may have symptoms related to this, such as palpitations, angina (if pre-existing heart disease is present), intermittent claudication of the legs, and symptoms of heart failure. Anemia can lead to a rapid or irregular heartbeat (arrhythmia) and an enlarged heart, which increses the risk of heart disease.')
        elif (cause=='Diabetes'):
            st.write('Diabetes is a disease that occurs when your blood glucose, also called blood sugar, is too high. Blood glucose is your main source of energy and comes from the food you eat. Insulin, a hormone made by the pancreas, helps glucose from food get into your cells to be used for energy. Sometimes your body doesn’t make enough—or any—insulin or doesn’t use insulin well. Glucose then stays in your blood and doesn’t reach your cells. Over time, having too much glucose in your blood can cause health problems among which is heart disease. Over time, high blood sugar can damage blood vessels and the nerves that control your heart, affecting the capability of your heart to pump blood through the system efficiently. ')
        elif (cause=='High blood pressure'):
            st.write('High blood pressure, also called hypertension, is blood pressure that is higher than normal. Your blood pressure changes throughout the day based on your activities. Having blood pressure measures consistently above normal may result in a diagnosis of high blood pressure (or hypertension). A normal blood pressure level is less than 120/80 mmHg. High blood pressure can damage your arteries by making them less elastic, which decreases the flow of blood and oxygen to your heart and leads to heart disease.')
        else :
            st.write('Smoking is a major cause of cardiovascular disease (CVD) and causes approximately one of every four deaths from CVD, according to the 2014 Surgeon General’s Report on smoking and health. CVD is the single largest cause of death in the United States, killing more than 800,000 people a year. More than 16 million Americans have heart disease. Almost 8 million have had a heart attack and 7 million have had a stroke. Chemicals in cigarette smoke cause the cells that line blood vessels to become swollen and inflamed. This can narrow the blood vessels and can lead to many cardiovascular conditions.')




#############




st.header('Heart failure in relation')
st.subheader('What is the relation of this comorbidity on death ?')

st.write('As we said, heart failure can sometimes be the source of death of some patients. In most cases, the deceased were suffering, in addition to heart failure, other diseases reinforcing the consequences of the first. We talk about comorbidities.')

comorbidity = st.selectbox(
    'Wish comorbidity would you like to investigate ? ',
    ('Age', 'Anaemia','Diabetes', 'High blood pressure', 'Smoking')
    )


if comorbidity == 'Age':
  histogram_comorbidity = px.histogram(df,x=comorbidity, color='Dead', barnorm = 'fraction', barmode='relative', title = 'Distribution of the morbidity in function of '+cause)
  st.plotly_chart(histogram_comorbidity)
else:
 histogram_comorbidity = px.histogram(df, x=comorbidity, color= 'Dead', barnorm = 'percent', barmode='relative', title = 'Distribution of the morbidity in function of '+comorbidity, text_auto = True)
 histogram_comorbidity.update_xaxes(type='category')
 st.plotly_chart(histogram_comorbidity)



df['Level_of_platelets']=df['Level of platelets']
df['Level_of_sodium']=df['Level of sodium']
df['High_Blood_Pressure'] = df['High blood pressure']
df['Ejection_fraction']=df['Ejection fraction']

mod =  smf.probit('Dead ~ Age +Anaemia + CPK + Diabetes +Ejection_fraction+High_Blood_Pressure+Level_of_platelets+Level_of_sodium+Sex+Smoking', data=df)
res = mod.fit()
marge_effect_comorbidity = res.get_margeff(at='mean', method='dydx')



with st.expander('Want to dig deeper into the causality between these two variables ?'): 
    st.write(marge_effect_comorbidity.summary())
    
    if (comorbidity=='Age'):
        st.write()
        st.write('The distribution of morbidity according to age shows us that the proportion of people who die increases with age.')
        st.write('Even if we cannot speak about comorbity, age remains an aggravating factor.')
        st.write('Indeed, it is estimated that taking one year of age increases the chances of death by about ',0.0119,'%.')
    elif (comorbidity=='Anaemia'):
        st.write()
        st.write('Interesting to see is that among patients suffering from Anaemia, the proportion of death patient is higher than amongst those who do not have this disease. When looking at the probit estimated coefficient we see a postivie value, yet not siginifcant it might give a hint of a possible negative influence of anaemia on the probabbility of surviving.')
    elif (comorbidity=='Diabetes'):
        st.write()
        st.write('We can see that the proportion of diabetics is the same if we look at the living and the dead. Thus, we can conclude that diabetes does not play a role in the outcome of heart failure. This intuition is confirmed when we apply a probit model, the diabetes variable fails to be significant.s')
    elif (comorbidity=='High blood pressure'):
        st.write()
        st.write('The proportion of people with high blood pressure is about 8% higher among the living than among the deceased.')
        st.write('This result is, to our previous explanations, counter intuitive. One would have thought that high blood pressure was an aggravating factor.')
        st.write('Nevertheless, the statistical examination of this variable does not manage to find any significance to this factor.') 
        st.write('Thus, it is possible to think that this increase is insignificant. It could simply be the result of a particular sample.')
    else :
        st.write()
        st.write('We can see that the proportion of smokers is the same if we consider the living and the dead. We can therefore conclude that diabetes does not play a role in the outcome of heart failure. This intuition is confirmed when we apply a probit model, the smoking variable is not significant.')




st.write('')
st.write('What is interesting to be noted is the fact that many combination of different diseases may make a detrimental cocktail of diseases which in combination significantely increase the probability of death. This investigation of different combinations in relation to heart failure remains a topic to be aware of and is unfortunately beyond the scope of our analysis. We happily leave this frontier to discover to our fellows academic collegues.')
st.write('')
st.write('')


#############


st.header('Understanding the death probability based on the sample and you !')

st.write("If you wish, you can fill out a fictitious heart failure patient file. On the basis of the information provided, we will establish the likelihood that the patient's vital prognosis is compromised.")
st.write('Notice that we assume that the patient already has a heart disease.')
st.write('Our analysis is based on a probit model. The performance of the model is as follows: ')
st.write('Note that we had only 299 observations to proceed to its training and its control.')

st.subheader('Create your own patient profile')



col1, col2 = st.columns(2)

with col1 :
    sex = st.radio('What is you birth sex ?',  options= ['Male','Female'])
    first_name = st.text_input('First Name')
    second_name = st.text_input('Second Name')
    age = st.number_input('Age', 0,99)
    smoke = st.radio('Do you smoke on a daily basis ? ',options= ['Yes', 'No'])
    health_issues = st.multiselect('Do you have any of theses conditions ?', ['Anaemia','Diabetes', 'High blood pressure', 'None'])

with col2: 
    CPK = st.slider('What is your CPK level ? ',0,5000)
    pourcentage_of_ejection_fraction = st.slider('What is your percentage of ejection fraction ?',0,100)
    level_of_platelets = st.slider('What is your level of platelets ?', 2000, 600000) 
    level_of_creatinine = st.slider('What is your level of creatinine ?', 0, 10) 
    level_of_sodium = st.slider('What is your level of sodium ?', 100,150)

# Creation of our variables :
    
name = first_name+' '+second_name
anaemia = [0]
diabetes = [0] 
high_blood_pressure = [0]
for value in  health_issues : 
    if value == 'Anaemia' : 
        anaemia = [1]
    elif value == 'Diabetes':
        diabetes = [1]
    elif value == 'High blood pressure':
        high_blood_pressure = [1]

# Need to be convert in nested loop 
if smoke =='Yes': 
    smoke = 1
else :
    smoke = 0

if sex =='Male': 
    sex = 1
else :
    sex = 0
    
# Creation of our new dataframe 
new_df = pd.DataFrame({'Age':age,
                   'Anaemia':anaemia ,
                   'CPK':CPK ,
                   'Diabetes':diabetes ,
                   'Percentage of ejection fraction':pourcentage_of_ejection_fraction,
                   'High blood pressure':high_blood_pressure,
                   'Level of platelets':level_of_platelets,
                   'Level of creatinine':level_of_creatinine,
                   'Level of sodium':level_of_sodium,
                   'Sex':sex,   
                   'Smoking':smoke})



####### MODEL PROBIT #########
df = pd.read_csv(url, sep=',')
df = pd.DataFrame(df)

df_X = df.drop(['DEATH_EVENT','time'],axis=1)
df_Y = df[['DEATH_EVENT']]

X_train, X_test, Y_train, Y_test = train_test_split(df_X, df_Y,test_size=0.3,random_state=0)

probit_model=sm.Probit(Y_train,X_train)
result_full=probit_model.fit()

marge_effect = result_full.get_margeff(at='mean', method='dydx')



####### Testing the model on new_df ######

params = pd.DataFrame(probit_model.fit().params,)

pourcentage = new_df['Age'] * params[0][0] + new_df['Anaemia'] * params[0][1] + new_df['CPK'] * params[0][2] + new_df['Diabetes'] * params[0][3] + new_df['Percentage of ejection fraction'] * params[0][4] + new_df['High blood pressure'] * params[0][5] + new_df['Level of platelets'] * params[0][6] + new_df['Level of creatinine'] * params[0][7] + new_df['Level of sodium'] * params[0][8] + new_df['Sex'] * params[0][9] + new_df['Smoking'] * params[0][10] 
pourcentage = pd.DataFrame(pourcentage)

####### Evaluation of probit model
print(result_full.summary())


result1 = X_test
result1['y_pred'] = result1['age'] * params[0][0] + result1['anaemia'] * params[0][1] + result1['creatinine_phosphokinase'] * params[0][2] + result1['diabetes'] * params[0][3] + result1['ejection_fraction'] * params[0][4] + result1['high_blood_pressure'] * params[0][5] + result1['platelets'] * params[0][6] + result1['serum_creatinine'] * params[0][7] + result1['serum_sodium'] * params[0][8] + result1['sex'] * params[0][9] + result1['smoking'] * params[0][10] 

import scipy.stats as si
def normsdist(z):
    z = si.norm.cdf(z,0.0,1.0)
    return (z)

result1["y_pred_Probit"] = normsdist(result1["y_pred"])



#### Decision rule to determine if patient is dead = 0 or 1
d = {'y_pred_proba': result1['y_pred_Probit']}
df23 = pd.DataFrame(data=d)
df23 = df23.reset_index()
df23.drop(['index'], axis=1, inplace=True)
df23['y_pred'] = 0.000
for i in range(0,len(df23['y_pred_proba'])):
    if df23['y_pred_proba'][i] > 0.45:
        df23['y_pred'][i] = 1.000
    else: 
        df23['y_pred'][i] = 0.000
y_pred = np.array(df23['y_pred'])
y_pred = y_pred.astype('int64')


result1["decision"] = y_pred
result1["actual"] = Y_test

print('Accuracy of Probit Model on test set: {:.2f}'.format(accuracy_score(Y_test, y_pred)))
confusion_matrix = confusion_matrix(Y_test, y_pred)


y_pred_proba = np.array(df23['y_pred_proba'])
probit_roc_auc = roc_auc_score(Y_test, y_pred)
fpr, tpr, thresholds = roc_curve(Y_test, y_pred_proba)
plt.figure()
plt.plot(fpr, tpr, label='Probit Model (area = %0.2f)' % probit_roc_auc)
plt.plot([0, 1], [0, 1],'r--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic')
plt.legend(loc="lower right")




####### Displaying our results 
with st.expander('Do you want to see the result of your patient ?'): 

    st.write('Your patient ', name,'has a', round(normsdist(pourcentage.iloc[0].squeeze())*100, 1), ' % probability of being under life-threatening conditions' )

with st.expander('Do you want to see behind the scenes of this prediction ? Watch out! It is getting spicy'):
    st.write('For the prediction we use the econometric Probit model to obtain a probability for our target variable "Dead". We decided against a classical Machine Learning model such as a Decision tree classifier as we wanted to obtain a probability of death given a specific set of independent variables and decompose the influence of the respective variables on the probability through the marginal effects.')
    st.write('To apply or translate the results into interpretable and applicable coefficients one need to apply the probit results on a normal distribution. This will output marginal probabilities of the predictors.')
    st.write('After obtaining the marginal probabilities of each predictor we multiply each marginal effect with the input values of each predictor and sum them up to obtain a final death probability which we see in the final output of the appliaction')
    st.write('Of course we weighted against a logit or a classical machine learning process by evaluating the accuracy of the model. Yet, this is not trivial as we obtain a probability in the Probit case, not a definied classification whether the patient is going to die or not given the inputs. Therefore it is necessary to define a rule of decision i.e. a probability threshold above which a patient in our sample is given a dead or alive decision. We decided to set that threshold arbitrarily to 45%. If a patient has a probability of over 45% to die, the model will predict that the patient will definetely die. This is of course subject of discussion if that threshold is properly choosen, yet experimentation showed that this threshold yields the best accuracy.')
    st.write('The accuracy of Probit Model on the test set is: ', round(accuracy_score(Y_test, y_pred)*100,1),'%')
    st.write('')
    st.write('These are the estimations of the Probit regression:')
    st.write(result_full.summary())
    st.write('')
    st.write('')
    st.write('Hereby we display some metrics to evaluate our model:')
    st.write('The confusion matrix:')
    st.write(confusion_matrix)
    st.write('')
    st.write('And the ROC curve:')
    st.pyplot(plt)
    
    
   
  

st.markdown('')
st.write('A Python project by Gaspard Boyer and Jan-Philipp Kretschmann')
st.write('Université Paris Dauphine - PSL , Master QEA')
          
    
