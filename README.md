# PlagueIncModel
## Ideas
We are trying to establish a model which could be used to predict the numbers of deaths and infective of the noovel Coronavirus outbreak in Wuhan, China. The model is based on kinetics and we've made some basic hypothesis.
### Categories of individuals
#### Susceptable, S
The healthy, uninfected crowd which have a probability of becoming the infective.
#### Exposed, E
#### Infective(Segregated), I0
#### Infective(Unsegregated), I1
#### Dead, D
#### Recovered, R
## Equations

### ![](http://latex.codecogs.com/gif.latex?I_1=k_NI)
### ![](http://latex.codecogs.com/gif.latex?I_{eff}=I_1+E)

## Kinetics

### ![](http://latex.codecogs.com/gif.latex?-\frac{dS}{dt}=\alpha%20SI_{eff})
### ![](http://latex.codecogs.com/gif.latex?\frac{dE}{dt}=\\alphaSI_{eff}-\\betaE)
### ![](http://latex.codecogs.com/gif.latex?\frac{dI}{dt}=\\betaE-(\\gamma+\\delta)I)
### ![](http://latex.codecogs.com/gif.latex?\frac{dR}{dt}=\\gamma)
### ![](http://latex.codecogs.com/gif.latex?\frac{dD}{dt}=\\deltaI)

## Data
### Data Source Announcement
The data shown below are all captured from the website of National Health Commission of PRC(中国国家卫生健康委员会 http://www.nhc.gov.cn/) and Local Health Commission in China(Wuhan, e.g.).
All figures are based on fact, if you have any question, please check the website above. Data is entered by hand, so there could be mistakes and please do correct us if so.

|Date |	Day |	Skeptical |	Comfirmed	Dead |	Cured |	DeathRatio |	CureRatio |	dD/dt |	dR/dt |
|---: |---: |---------: |--------------: |------: |-----------:|-----------:|------:|-----: |
|2020/1/5|	5|	0|	59|	0|	0|	0.0%|	0.0%|		||
|2020/1/11|	7|	0|	41|	1|	4|	2.4%|	9.8%|	0.5| 	2.0| 
|2020/1/15|	15|	0|	41|	2|	12|	4.9%|	29.3%|	0.1| 	1.0| 
|2020/1/16|	16|	0|	45|	2|	15|	4.4%|	33.3%|	0.0| 	3.0|
|2020/1/17|	17|	0|	62|	2|	19|	3.2%|	30.6%|	0.0| 	4.0 |
|2020/1/18|	18|	0|	121|	3|	24|	2.5%|	19.8%|	1.0| 	5.0| 
|2020/1/19|	19|	0|	198|	3|	25|	1.5%|	12.6%|	0.0| 	1.0 |
|2020/1/20|	20|	54|	291|	6|	25|	2.1%|	8.6%|	3.0| 	0.0 |
|2020/1/21|	21|	37|	440|	9|	28|	2.0%|	6.4%|	3.0| 	3.0 |
|2020/1/22|	22|	393|	571|	17|	28|	3.0%|	4.9%|	8.0| 	0.0| 
|2020/1/23|	23|	1072|	830|	25|	34|	3.0%|	4.1%|	8.0| 	6.0 |
|2020/1/24|	24|	1965|	1303|	41|	38|	3.1%|	2.9%|	16.0| 	4.0| 
|2020/1/25|	25|	2684|	1975|	56|	49|	2.8%|	2.5%|	15.0| 	11.0| 
|2020/1/26|	26|	5794|	2762|	80|	51|	2.9%|	1.8%|	24.0| 	2.0 |

## Current Progress
### Death Rate - Infective Graph
We first drew a curve of death rate against infective, and we find a strong linear relativity between these two variables. The graph is shown below.
![avatar](https://github.com/ShiZhuming/PlagueIncModel/blob/master/Cache/2019-nCoV%E6%AD%BB%E4%BA%A1%E7%8E%87-%E7%A1%AE%E8%AF%8A%E4%BA%BA%E6%95%B0.jpg)
Then we drew a curve of the cured against time, and we found a strong linear relativity between them, which means the cured is steadily increasing with time.
### Cured Crowds - Time Graph
![avatar](https://github.com/ShiZhuming/PlagueIncModel/blob/master/Cache/2019-nCoV%E6%B2%BB%E6%84%88%E4%BA%BA%E6%95%B0-%E6%97%B6%E9%97%B4.jpg)
### Cure Rate - Infective Graph
![avatar](https://github.com/ShiZhuming/PlagueIncModel/blob/master/Cache/2019-nCoV%E6%B2%BB%E6%84%88%E7%8E%87-%E7%A1%AE%E8%AF%8A%E4%BA%BA%E6%95%B0.jpg)
### Basic Statistics
This graph contains the basic statistics of the 2019-nCoV plague originated from Wuhan, Hubei Prov., China. Deathrate is illustrated as red line according to the right axis, and the infective(comfimred and uncomfirmed), death are illustrated in lines with data dots.
![avatar](https://github.com/ShiZhuming/PlagueIncModel/blob/master/Cache/2019-nCoV%E7%96%AB%E6%83%85%E7%BB%9F%E8%AE%A1.jpg)
