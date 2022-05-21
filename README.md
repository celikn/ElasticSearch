# Elastic Search ve Kibana
## _Kibana Notları_
Veri analiz ve görselleştirmede kullanılan bir araçtır Elasticsearch ile birlikte kullanılır.Elasticsearch clusterlarının izlenmesi,yönetilmesi gibi işlemlerin merkezleştirildiği yapılar sağlar.
- log ve log analizi 
- altyapı metrikleri ve container yönetimi
- geospatial veri analizi ve görselleştirme
- güvenlik analizleri 

ElasticSearch üzerinde index ler üzerinde veri sorgulama ve Lens,Canvas ve Map ile görselleştirme sağlayabilmekte. 

Kibana da dashboard olusturabilmek icin Elasticsearch icinde index bulunmalidir. 
## ElasticSearch 

Elasticsearch bir node uzerinde calisir. Bu nodun Unique id si ve ait oldugu bir cluster vardir. Farkli makinalarda farkli nodelar uzerinde elasticsearch calisiyor olabilir. Bu nodlarin ait oldugu bir  cluster olabilir 

<img src="Img/ElasticSearchClusters.png"/>


Veriler document olarak Json objesi formatinda tutulur. Her bir document bir unique id ye sahiptir.
```
{ name :"Clementines",
  category:"Fruits",
  brand:"Cuties",
  price:"$4.29"
```  

Benzer Dokumanlar Indexler halinde grouplanir. 

<img src="Img/DocumentGroupIntoIndex.png"/>

Bir index birden fazla node a bagli olabilir. Ve ilgili index in bir node icindeki parcasina shard diyoruz.
<img src="Img/Shard.png"/>

Ornegin bir makinadaki shard 200bin veri tutabiliyor. 600 bin veri tutabilmek icin farkli nodelarda ek shardlar olusturulabilir. Veriler attikca yatay olarak shardlari tutacagimiz nodelari arttirabiliriz. 





Bir index olustugunda bir shard otomatik olarak olusur. Fakat ilgili configuration yapilarak birden fazla shard olusturulabilir. 

Ornegin bir makinadaki shard 200bin veri tutabiliyor. 600 bin veri tutabilmek icin farkli nodelarda ek shardlar olusturulabilir. Veriler attikca horizontally olarak shardlari tutacagimiz nodelari arttirabiliriz. 

<img src="Img/SingleShard.png"/>

Diyelim ki tum verilerimizi tek bir shard icinde 500k olarak tutuyoruz. Sequential Search 10 sn suruyor. Bu verileri farkli nodelarda dagitirsak ornegin 10 node ve her shard 50k veri tutuyorsa bu durumda 1sn surede paralel olarak 1sn surecektir. 

<img src="Img/ShardingAcrossNodes.png"/>

