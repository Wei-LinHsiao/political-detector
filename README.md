# political-detector
Logistic regression model to detect American political party slanting.

Data crawled from reddit.com.

Final Results:

```
precision    recall  f1-score   support

0.0       0.78      0.91      0.84      1331
1.0       0.78      0.55      0.64       746

micro avg       0.78      0.78      0.78      2077
macro avg       0.78      0.73      0.74      2077
weighted avg       0.78      0.78      0.77      2077

Accuracy:  0.7823784304285026
F1 Score:  0.8431644691186677

Words/ Phrases most associated with Democratic Party:
[u'bernie', u'sanders', u'dnc', u'democratic', u'vote', u'progressive', u'republicans', u'campaign', u'delegates', u'bernies', u'primary', u'hillary', u'candidate', u'clinton', u'money', u'tax', u'party', u'politician', u'run', u'military', u'state', u'pay', u'convention', u'candidates', u'corporate', u'healthcare', u'congress', u'shes', u'poll', u'need', u'running', u'speeches', u'lost', u'hrc', u'position', u'revolution', u'senator', u'democrats', u'absolutely', u'just', u'supporters', u'justice', u'rich', u'100', u'look', u'gop', u'doesnt', u'primaries', u'voters', u'warren']

Words/ Phrases most associated with Republican Party:
[u'reddit', u'liberals', u'mr', u'white', u'liberal', u'conservatives', u'maga', u'mr trump', u'uspez', u'racist', u'conservative', u'admins', u'left', u'japan', u'spez', u'women', u'violence', u'antifa', u'posts', u'comey', u'fbi', u'black', u'muslim', u'immigration', u'censorship', u'trump', u'rthe_donald', u'emails', u'post', u'cucks', u'racism', u'gender', u'girl', u'coat', u'refugees', u'america great', u'banned', u'crying', u'cuck', u'rall', u'gay', u'men', u'deleted', u'car', u'sjw', u'asians', u'fucking', u'hitler', u'japanese', u'countries']

```
