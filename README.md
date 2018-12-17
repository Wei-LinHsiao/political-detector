# political-detector
Logistic regression model to detect American political party slanting.

Data crawled from reddit.com.

Final Results:

```
              precision    recall  f1-score   support

         0.0       0.80      0.90      0.85      1367
         1.0       0.76      0.57      0.65       710

   micro avg       0.79      0.79      0.79      2077
   macro avg       0.78      0.74      0.75      2077
weighted avg       0.79      0.79      0.78      2077

Accuracy:  0.7905633124699085
F1 Score:  0.8503611971104231

Words/ Phrases most associated with Democratic Party: 
[u'bernie', u'sanders', u'vote', u'dnc', u'progressive', u'democratic', u'campaign', u'republicans', u'primary', u'party', u'delegates', u'hillary', u'bernies', u'money', u'candidate', u'military', u'tax', u'healthcare', u'clinton', u'pay', u'state', u'hrc', u'politician', u'run', u'corporate', u'need', u'voting', u'revolution', u'wont', u'poll', u'speeches', u'establishment', u'congress', u'senator', u'justice', u'choice', u'supporters', u'convention', u'way', u'running', u'general', u'doesnt', u'coverage', u'hes', u'people', u'delegate', u'position', u'edit', u'lost', u'scandal']

Words/ Phrases most associated with Republican Party: 
[u'reddit', u'liberal', u'white', u'mr', u'liberals', u'conservative', u'mr trump', u'admins', u'maga', u'conservatives', u'uspez', u'japan', u'spez', u'left', u'racist', u'women', u'muslim', u'antifa', u'posts', u'censorship', u'trump', u'black', u'cuck', u'fbi', u'racism', u'comey', u'refugees', u'america great', u'asians', u'men', u'violence', u'gender', u'cucks', u'rthe_donald', u'hillary clinton', u'immigration', u'hitler', u'car', u'rall', u'make america', u'countries', u'sides', u'post', u'japanese', u'leftist', u'immigrants', u'male', u'fucking', u'emails', u'color']

```
