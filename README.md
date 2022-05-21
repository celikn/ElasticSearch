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

ElasticSearch REST API uzerinden clusterlara erismemizi ve iletisim saglayabilmemize olanak saglar. Search request gonderdigimizde HTTP request port 9200 a gider. Ilgili portta calisan elasticsearch e request yolladigimizda bize cluster ve elasticSearch versiyon bilgisi geri gonderir. 

```
curl localhost:9200
```

```
{
  "name" : "4d899444b95a",
  "cluster_name" : "docker-cluster",
  "cluster_uuid" : "sGgxn3BVTp-Ji546RVG7Yw",
  "version" : {
    "number" : "8.2.0",
    "build_flavor" : "default",
    "build_type" : "docker",
    "build_hash" : "b174af62e8dd9f4ac4d25875e9381ffe2b9282c5",
    "build_date" : "2022-04-20T10:35:10.180408517Z",
    "build_snapshot" : false,
    "lucene_version" : "9.1.0",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```

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

Fakat birden fazla node uzerinde tututulan durumda nodlardan biri giderse, verileri kaybetmis oluruz. Bu yuzden nodelarda tutulan shardlarin ikinci kopyalarini baska bir node uzerinde tutabiliriz. Bunlara primary shard ve replica shard deriz. Eger replica shard varsa bu search islemini de hizlandirir. Bir saniyede 8000 query geldigi bir durum dusunuldugunde eger replica shard varsa bazi destek saglayabilir. 


[CrashCourceGit](https://github.com/LisaHJung/Beginners-Crash-Course-to-Elastic-Stack-Series-Table-of-Contents)
[Beginner](https://github.com/LisaHJung/Part-1-Intro-to-Elasticsearch-and-Kibana)


Calisan clusterlarin saglik durumunu incelemek icin 

```
curl -u elastic:changeme http://localhost:9200/_cat/health 
```

ElasticSerch uzerinde olusturcagimiz cluster ve node lari daha anlamli isimler ile degistirmekte yarar var. Ozellikle clusterlar buyudukce bu gereklilik olusturuyor. (bu islemi yaml elasticsearch un kurulu oldugu folder altinda bulunan yaml dosyasi icindeki cluster.name ve node.name  parameteresini degistirerek yapabliriz. Bu islemler sonrasinda elasticsearch ve kabana yeniden baslatilmali)


## Request Gonderme

Kabana localhost:5601 uzerinde calisiyor. 

Management->DevTools menusunde Console bulunmakta. 

Bulunan cluster larimiz hakkindaki health bilgisini getirmek icin 

```
GET _cluster/health

{
  "cluster_name" : "docker-cluster",
  "status" : "green",
  "timed_out" : false,
  "number_of_nodes" : 1,
  "number_of_data_nodes" : 1,
  "active_primary_shards" : 8,
  "active_shards" : 8,
  "relocating_shards" : 0,
  "initializing_shards" : 0,
  "unassigned_shards" : 0,
  "delayed_unassigned_shards" : 0,
  "number_of_pending_tasks" : 0,
  "number_of_in_flight_fetch" : 0,
  "task_max_waiting_in_queue_millis" : 0,
  "active_shards_percent_as_number" : 100.0
}

```

Bulunan nodelar ve hakkindaki bilgilere erismek icin 

```
GET _nodes/stats


{
  "_nodes" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "cluster_name" : "docker-cluster",
  "nodes" : {
    "sTmt1bClSAeachl428phwA" : {
      "timestamp" : 1653169355697,
      "name" : "4d899444b95a",
      "transport_address" : "172.18.0.2:9300",
      "host" : "172.18.0.2",
      "ip" : "172.18.0.2:9300",
      "roles" : [
        "data",
        "data_cold",
        "data_content",
        "data_frozen",
        "data_hot",
        "data_warm",
        "ingest",
        "master",
        "ml",
        "remote_cluster_client",
        "transform"
      ],
      "attributes" : {
        "ml.max_jvm_size" : "5343543296",
        "xpack.installed" : "true",
        "ml.machine_memory" : "10685800448"
      },
      "indices" : {
        "docs" : {
          "count" : 271,
          "deleted" : 7566
        },
        "shard_stats" : {
          "total_count" : 8
        }
        ...
}

```