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

- Index olusturma (asagida favorite_candy adinda bir index olusturduk) `Syntax : PUT Name-of-the-Index`

```
PUT favorite_candy

{
  "acknowledged" : true,
  "shards_acknowledged" : true,
  "index" : "favorite_candy"
} 

```

- Olusturdugumuz index e bir dokuman ekleyelim. 

```
POST Name-of-the-Index/_doc
{
  "field": "value"
}
```

Hem post hem put kullanilabilir. Post kullanildiginda elasticsearch automatik olarak id olusturur dokuman icin. POST ardindan index adi ve `_doc` keyword ile birlikte json formatindaki dokumani gonderiyoruz. Bize auto generated id ile donus yapar. 

```
POST favorite_candy/_doc
{
  "first_name": "Lisa",
  "candy": "Sour Skittles"
}

{
  "_index" : "favorite_candy",
  "_id" : "ohei6IABIUJON3OvB1B7",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 0,
  "_primary_term" : 1
}
```

```
PUT Name-of-the-Index/_doc/id-you-want-to-assign-to-this-document
{
  "field": "value"
}
```

```
PUT favorite_candy/_doc/1
{
  "first_name": "John",
  "candy": "Starburst"
}

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 1,
  "result" : "created",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 1,
  "_primary_term" : 1
}
```

Ozellikle hastalarin oldugu bir veride idlerin autogenerate olmamasi daha anlamli olabilir. 

- Kayitlari okuma `GET Name-of-the-Index/_doc/id-of-the-document-you-want-to-retrieve`

```
GET favorite_candy/_doc/1

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 1,
  "_seq_no" : 1,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "first_name" : "John",
    "candy" : "Starburst"
  }
}

```

Bir dokumani mevcut olan bir id ile ekledigimizde
versiyon 2 olarak geri donus olur ve veri update edilir. Versiyon bir verinin kac kez create,update yada delete oldugunu belirtir. 

```
PUT favorite_candy/_doc/1
{
  "first_name": "John2",
  "candy": "Starburst2"
}

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 2,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 4,
  "_primary_term" : 1
}
```

Ayni id ye sahip dokumana tekrar get request yaparsak, source bilgisi overwrite yapilmis oldugunu goruruz. Fakat bu pek istenen bir durum degil.

```
GET favorite_candy/_doc/1
{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 2,
  "_seq_no" : 4,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "first_name" : "John2",
    "candy" : "Starburst2"
  }
}
```

Bu yuzden `_create` keyword unu kullaniriz. 

- Create dokuman 

```
PUT Name-of-the-Index/_create/id-you-want-to-assign-to-this-document
{
  "field": "value"
}
```

Mevcut bir id ile dokuman create etmeye calisirsak bize hata mesaji ile donecektir. 


```
PUT favorite_candy/_create/1
{
  "first_name": "Finn",
  "candy": "Jolly Ranchers"
}

{
  "error" : {
    "root_cause" : [
      {
        "type" : "version_conflict_engine_exception",
        "reason" : "[1]: version conflict, document already exists (current version [2])",
        "index_uuid" : "CtC5ZKxdRt2nNwin9IxemA",
        "shard" : "0",
        "index" : "favorite_candy"
      }
    ],
    "type" : "version_conflict_engine_exception",
    "reason" : "[1]: version conflict, document already exists (current version [2])",
    "index_uuid" : "CtC5ZKxdRt2nNwin9IxemA",
    "shard" : "0",
    "index" : "favorite_candy"
  },
  "status" : 409
}
```

- Update islemi icin `_update` keyword unu kullaniyoruz.

Mevcut bir veriyi sadece bazi belirli field lari kullanarak guncellemek istiyorsak
```
POST Name-of-the-Index/_update/id-of-the-document-you-want-to-update
{
  "doc": {
    "field1": "value",
    "field2": "value",
  }
} 
```


```
POST favorite_candy/_update/1
{
  "doc": {
    "candy": "M&M's"
  }
}

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 3,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 5,
  "_primary_term" : 1
}

POST favorite_candy/_update/1
{
  "doc": {
    "sonradaneklenenfield": "bisey"
  }
}

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 4,
  "result" : "updated",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 6,
  "_primary_term" : 1
}


```
Son durumda hem update etmek istedigimiz fieldlari goruyoruz hem de update ile yeni ekledigimiz fieldlari

```
GET favorite_candy/_doc/1

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 4,
  "_seq_no" : 6,
  "_primary_term" : 1,
  "found" : true,
  "_source" : {
    "first_name" : "John2",
    "candy" : "M&M's",
    "sonradaneklenenfield" : "bisey"
  }
}
```

Eger bir veriyi silmek istiyorsak `_delete` keyword unu kullaniyoruz. `DELETE Name-of-the-Index/_doc/id-of-the-document-you-want-to-delete`

```
DELETE favorite_candy/_doc/1

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "_version" : 5,
  "result" : "deleted",
  "_shards" : {
    "total" : 2,
    "successful" : 1,
    "failed" : 0
  },
  "_seq_no" : 7,
  "_primary_term" : 1
}

GET favorite_candy/_doc/1

{
  "_index" : "favorite_candy",
  "_id" : "1",
  "found" : false
}
```


##Search in ElasticSearch 

ElasticSearch aramalarindan gelen siralama scoring algorithmalari ile belirleniyor. (precision ve recall)

Bir dokumentin score unu hesaplarken Term Frequency (bir term un dokuman icinde kac kez gectigini) bilgisini kullanir. Fakat en cok term gecen dokuman her zaman en relevant dokuman olmaz.


Default algoritma :  Practical Scoring Algoritmasi 

Term Frequency (tf): bir term un dokuman field inde gorunme sayisinin karekoku. (Bir term ne kadar cok varsa o kadar relevant oldugunu varsayar.)

```
tf = sqrt(termFreq)
```

Inverse Document Frequency (IDF): toplam belge saysinin  term i iceren belge sayisina bolumunun log degerini alir. Bir term ne kadar cok dokumanda geciyorsa o term o kadar az onemlidir varsayimi yapmis oluruz.

```
idf = 1 + ln(maxDocs/(docFreq + 1))
```

Coordination (coord):sorguda istenen terim lerin gelen dokumandaki sayisidir. Query termlerinin hepsi iceren dokuman bazilarini icerenlere gore daha fazla scora sahip olacaktir. 

Field length normalization (norm): terimlerin sayisinin karekokunun tersidir. 

```
norm = 1/sqrt(numFieldTerms)
```

Query normalization (queryNorm): 

Index boost: bir alandaki (field) score u arttirmak icin kullanilan sayidir. 

Query boost: bir sorgu tumcesi (query clause) score unu arttirmak icin kullanilan sayidir. 

.... 

- Bir field icinde arama, match query type inin icerisine ilgili field ve aramak istedigim term i yaziyoruz.

```
GET nyc-restaurants/_search
{
  "track_total_hits": true,
  "size": 2,
   "query" : {
      "match" : {
         "violation_description" : "Harborage"
      }
   }
}
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2281,
      "relation" : "eq"
    },
    "max_score" : 2.3678188,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50111367",
        "_score" : 2.3678188,
        "_source" : {
          "name" : "COLUMBUS CEAFOOD",
          "borough" : "Manhattan",
          "cuisine" : "Seafood",
          "grade" : "A",
          "violation" : "08A",
          "violation_description" : "Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist.",
          "inspection_date" : "12/09/2021",
          "location" : {
            "lat" : 40.798059538144,
            "lon" : -73.963719548682
          }
        }
      }
    ]
  }
}
```

- birden fazla field icinde arama , multi_match  search tipinde fieldleri liste olarak belirtiyoruz. 

```
GET nyc-restaurants/_search
{
  "track_total_hits": true,
  "size": 2,
  "query": {
    "multi_match": {
      "query": "San",
      "fields": ["name", "cuisine"]
    }
  }
}
```


- tum fieldlerde arama , bu durumda multi_match query tipini kullaniyoruz. 

```
GET nyc-restaurants/_search
{
  "track_total_hits": true,
  "size": 10,
   "query": {
    "multi_match": {
      "query": "test"
    }
  }
}


{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 12.922431,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50111769",
        "_score" : 12.922431,
        "_source" : {
          "name" : "TEST KITCHEN",
          "borough" : "Manhattan",
          "cuisine" : "",
          "grade" : null,
          "violation" : "",
          "violation_description" : "",
          "inspection_date" : "01/01/1900",
          "location" : {
            "lat" : 40.714521963959,
            "lon" : -74.015677098865
          }
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "50117761",
        "_score" : 11.023067,
        "_ignored" : [
          "violation_description.keyword"
        ],
        "_source" : {
          "name" : "MOMO TEST KITCHEN",
          "borough" : "Brooklyn",
          "cuisine" : "Japanese",
          "grade" : "N",
          "violation" : "10F",
          "violation_description" : "Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit.",
          "inspection_date" : "01/28/2022",
          "location" : {
            "lat" : 40.646052086828,
            "lon" : -74.024096817066
          }
        }
      }
    ]
  }
}
```
- bool query  Elasticsearch must AND, should OR, must-not NOT olarak yaziliyor. 



Ornegin asagidaki sorguda, ilce  Manhattan ve cuisine Japanise olan ve B grade restorantlardan, violation description icerisinde sanitization mice food olamayanlari getiriyoruz. 

```
GET nyc-restaurants/_search
{
   "track_total_hits": true,
  "query": {
    "bool": {
      "must": [
      {
          "bool": {
            "must": [
              {
                "match": {
                  "borough": "Manhattan"
                }
              },
              {
                "match": {
                  "cuisine": "Japanese"
                }
              },
              {
                "match": {
                  "grade": "B"
                }
              }
            ]
          }
        }
     ],
      "must_not": [
        {
          "bool": {
            
            "should": [
             
              {
                "match": {
                  "violation_description":"sanitization mice food"
                }
                
              }
            ]
          }
        }
      ]
    }
  }
}



{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 4,
      "relation" : "eq"
    },
    "max_score" : 6.3899126,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50071943",
        "_score" : 6.3899126,
        "_source" : {
          "name" : "RAKU RESTAURANT",
          "borough" : "Manhattan",
          "cuisine" : "Japanese",
          "grade" : "B",
          "violation" : "09B",
          "violation_description" : "Thawing procedures improper.",
          "inspection_date" : "09/05/2019",
          "location" : {
            "lat" : 40.727313618727,
            "lon" : -74.002738428623
          }
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "41689018",
        "_score" : 6.3899126,
        "_source" : {
          "name" : "COCORON",
          "borough" : "Manhattan",
          "cuisine" : "Japanese",
          "grade" : "B",
          "violation" : "08A",
          "violation_description" : "Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist.",
          "inspection_date" : "07/09/2018",
          "location" : {
            "lat" : 40.720739838674,
            "lon" : -73.995295708372
          }
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "40951329",
        "_score" : 6.3899126,
        "_source" : {
          "name" : "TAKAHACHI TRIBECA",
          "borough" : "Manhattan",
          "cuisine" : "Japanese",
          "grade" : "B",
          "violation" : "06F",
          "violation_description" : "Wiping cloths soiled or not stored in sanitizing solution.",
          "inspection_date" : "03/01/2022",
          "location" : {
            "lat" : 40.716424879968,
            "lon" : -74.008015534265
          }
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "40911251",
        "_score" : 6.3899126,
        "_source" : {
          "name" : "SUSHI SEKI",
          "borough" : "Manhattan",
          "cuisine" : "Japanese",
          "grade" : "B",
          "violation" : "08A",
          "violation_description" : "Facility not vermin proof. Harborage or conditions conducive to attracting vermin to the premises and/or allowing vermin to exist.",
          "inspection_date" : "06/28/2017",
          "location" : {
            "lat" : 40.761816699614,
            "lon" : -73.960360575653
          }
        }
      }
    ]
  }
}


```

- dogru yazilmamis search termleri getirmek icin fuzzy query kullanilabilir. Asagidaki query de violation ve name field larinda RSTAUANT gecen termleri aradigimizda (_source ile sadece result icinde gecmesini istedigimiz field olarak "name" belirttik) bize 2627 sonuc donecektir. fuzziness parametresi kaldirildiginda hits listesi bos donecektir. 


```
GET nyc-restaurants/_search
{
   "track_total_hits": true,
   "size":2,
    "query": {
        "multi_match" : {
            "query" : "RSTAURANT",
            "fields": ["violation", "name"],
            "fuzziness": "AUTO"
        }
    },
    "_source": ["name"]
}

{
  "took" : 12,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2627,
      "relation" : "eq"
    },
    "max_score" : 2.0502763,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50093483",
        "_score" : 2.0502763,
        "_source" : {
          "name" : "RESTAURANT"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "50118538",
        "_score" : 1.6969975,
        "_source" : {
          "name" : "347 RESTAURANT"
        }
      }
    ]
  }
}


```

- partial terms - wildcard ve regex ornegi

```
GET  nyc-restaurants/_search
{
  "query": {

     "bool": {
      "must": [
        {
          "wildcard": {
            "violation_description": {
              "value": "*acceptable"
            }
          }
          
        },
        {
          "wildcard": {
            "cuisine": {
              "value": "Japan*"
            }
          }
          
        }, 
        {
           "regexp" : {
            "name" : "[a-z]*kitchen"
        }
        }
       
      ],
      "must_not": [
        {
          "term": {
            "violation_description": {
              "value": ""
            }
          }
        }
     ]
     }
    },
    "_source": ["name","grade","violation_description"]
}


{
  "took" : 5,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 3.0,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50117761",
        "_score" : 3.0,
        "_ignored" : [
          "violation_description.keyword"
        ],
        "_source" : {
          "grade" : "N",
          "name" : "MOMO TEST KITCHEN",
          "violation_description" : "Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit."
        }
      }
    ]
  }
}

```

- match phrase - query yapilan sozcukler ayni order da bulunmali (arada fazla bosluk yada karakter olmasi olmasi etkilemiyor)

```
GET nyc-restaurants/_search
{
   "track_total_hits": true,
   "size":2,
    "query": {
         "match_phrase": {
            "violation_description":"contact surface"
      }
    },
    "_source": ["name"]
}

{
  "took" : 23,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 6625,
      "relation" : "eq"
    },
    "max_score" : 3.8637352,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50112711",
        "_score" : 3.8637352,
        "_source" : {
          "name" : "PUPUSERIA IZALCO RESTAURANT"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "50118281",
        "_score" : 3.8637352,
        "_source" : {
          "name" : "NOSTRAND AVE PIZZA"
        }
      }
    ]
  }
}

```


- range query time (veri string olarak atildiginda zamana gore range query hits bos donmekte)
```
GET nyc-restaurants/_search
{
    "query": {
        "range" : {
            "inspection_date": {
                "gte": "2010-01-01",
                "lte": "2015-12-31"
            }
        }
    },
    "_source" : ["name","inspection_date"]
}


{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 6,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50017716",
        "_score" : 1.0,
        "_ignored" : [
          "violation_description.keyword"
        ],
        "_source" : {
          "name" : "TSION CAFE & BAKERY",
          "inspection_date" : "2015-12-23"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "40482599",
        "_score" : 1.0,
        "_source" : {
          "name" : "SCHOENFIELD",
          "inspection_date" : "2015-11-20"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "41412172",
        "_score" : 1.0,
        "_source" : {
          "name" : "EAT-A-BAGEL (JOHN A NOBLE FERRY BOAT)",
          "inspection_date" : "2013-06-07"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "50015538",
        "_score" : 1.0,
        "_source" : {
          "name" : "AMERICAN AIRLINES THEATER",
          "inspection_date" : "2015-11-19"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "50015171",
        "_score" : 1.0,
        "_source" : {
          "name" : "NEW AMSTERDAM THEATER",
          "inspection_date" : "2015-11-20"
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "41611709",
        "_score" : 1.0,
        "_source" : {
          "name" : "EQUESTRIS",
          "inspection_date" : "2015-12-12"
        }
      }
    ]
  }
}
```

- geoquery geo_distance ile merkez noktasindan belirli bir uzakliktaki verileri, geo_bounding_box rectangle icerisindeki verileri, geo_polygon, bir poligon icindekileri getirmemizi saglar.
geo_shape ise within yerine, intersect yada do not intesect query si yapmamizi sagliyor. 

```
GET nyc-restaurants/_search
{
  "size": 2, 
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_distance": {
          "distance": "300m",
          "location": {
            "lat": 40.7405,
            "lon": -74.005
          }
        }
      }
    }
  },
  "_source": ["name","location"]
}

{
  "took" : 8,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 131,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50103188",
        "_score" : 1.0,
        "_ignored" : [
          "violation_description.keyword"
        ],
        "_source" : {
          "name" : "STARBUCKS COFFEE #678 HUDSON",
          "location" : {
            "lon" : -74.005182035446,
            "lat" : 40.740502128064
          }
        }
      },
      {
        "_index" : "nyc-restaurants",
        "_id" : "50117118",
        "_score" : 1.0,
        "_source" : {
          "name" : "LA DEVOZIONE",
          "location" : {
            "lon" : -74.004713006739,
            "lat" : 40.741869040229
          }
        }
      }
    ]
  }
```

##Aggregation  

Veriyi ozetleyen metric ve istatistikleri olusturmamizi sagliyor. 

Sorgu aggregation kisminda ilgi belirtilen field e gore buckets icerisinde dokuman sayisini verir. 

```
GET nyc-restaurants/_search
{
  "aggs": {
    "by_category": {
      "terms": {
        "field": "cuisine",
        "size": 100
      }
    }
  }
}

...
"aggregations" : {
    "by_category" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 9984,
      "buckets" : [
        {
          "key" : "American",
          "doc_count" : 4797
        },
        {
          "key" : "",
          "doc_count" : 4017
        },
        {
          "key" : "Chinese",
          "doc_count" : 2151
        },
        {
          "key" : "Coffee/Tea",
          "doc_count" : 1715
        },
        {
          "key" : "Pizza",
          "doc_count" : 1536
        },
        {
          "key" : "Italian",
          "doc_count" : 947
        },
        {
          "key" : "Japanese",
          "doc_count" : 852
        },
        {
          "key" : "Mexican",
          "doc_count" : 827
        },
        {
          "key" : "Latin American",
          "doc_count" : 789
        },
        {
          "key" : "Bakery Products/Desserts",
          "doc_count" : 772
        }
      ]
...

```

- Query ve aggration kombinasyonlari

```
GET nyc-restaurants/_search
{
  "query": {
    "bool": {
      "must": {
        "match_all": {}
      },
      "filter": {
        "geo_distance": {
          "distance": "300m",
          "location": {
            "lat": 40.7405,
            "lon": -74.005
          }
        }
      }
    }
  },
  
  "aggs": {
    "by_category": {
      "terms": {
        "field": "cuisine",
        "size": 10
      }
    }
  }
}



{
  "took" : 15,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 131,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "nyc-restaurants",
        "_id" : "50103188",
        "_score" : 1.0,
        "_ignored" : [
          "violation_description.keyword"
        ],
        "_source" : {
          "name" : "STARBUCKS COFFEE #678 HUDSON",
          "borough" : "Manhattan",
          "cuisine" : "Coffee/Tea",
          "grade" : "A",
          "violation" : "10F",
          "violation_description" : "Non-food contact surface improperly constructed. Unacceptable material used. Non-food contact surface or equipment improperly maintained and/or not properly sealed, raised, spaced or movable to allow accessibility for cleaning on all sides, above and underneath the unit.",
          "inspection_date" : "2022-05-04",
          "location" : {
            "lat" : 40.740502128064,
            "lon" : -74.005182035446
          }
        }
      }
    ]
  },
  "aggregations" : {
    "by_category" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 30,
      "buckets" : [
        {
          "key" : "American",
          "doc_count" : 40
        },
        {
          "key" : "",
          "doc_count" : 16
        },
        {
          "key" : "Coffee/Tea",
          "doc_count" : 8
        },
        {
          "key" : "Italian",
          "doc_count" : 7
        },
        {
          "key" : "Bakery Products/Desserts",
          "doc_count" : 6
        },
        {
          "key" : "French",
          "doc_count" : 6
        },
        {
          "key" : "Pizza",
          "doc_count" : 6
        },
        {
          "key" : "Asian/Asian Fusion",
          "doc_count" : 4
        },
        {
          "key" : "Chinese",
          "doc_count" : 4
        },
        {
          "key" : "Mexican",
          "doc_count" : 4
        }
      ]
    }
  }
}

```
Precision arttirmak icin query yapilan birden fazla kelimeyi "operator":"and" parametresi ile arayabiliriz. 
```

GET nyc-restaurants/_search
{
  "size": 3, 
  "query": {
    "match": {
      "violation_description": {
        "query": "mice cockroach",
        "operator": "and"
      }
    }
  }
}


```