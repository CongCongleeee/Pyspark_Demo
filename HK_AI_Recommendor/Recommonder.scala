import java.io.PrintWriter

import org.apache.log4j.{Level, Logger}
import org.apache.spark.mllib.classification.{LogisticRegressionWithLBFGS, LogisticRegressionModel, LogisticRegressionWithSGD}
import org.apache.spark.mllib.linalg.SparseVector
import org.apache.spark.mllib.optimization.SquaredL2Updater
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.rdd.RDD
import org.apache.spark.{SparkContext, SparkConf}

import scala.collection.Map

/**
  * Created by root on 2016/5/12 0012.
  */
class Recommonder {

}

object  Recommonder{
  def main(args: Array[String]) {
    Logger.getLogger("org.apache.spark").setLevel(Level.ERROR)
    val conf = new SparkConf().setAppName("recom").setMaster("local")
    val sc = new SparkContext(conf)
    //加载数据，用\t分隔开
    //[['-1', 'Item.id,hitop_id6:1;Item.screen,screen4:1;Item.name,ch_name89:1;All,0:1;Item.author,author19:1;Item.sversion,sversion0:1;Item.network,x:1;Item.dgner,designer18:1;Item.icount,6:1;Item.stars,5.56:1;Item.comNum,11:1;Item.font,font5:1;Item.price,4593:1;Item.fsize,2:1;Item.ischarge,0:1;Item.downNum,50:1;User.Item*Item,hitop_id10*hitop_id6:1;User.Item*Item,hitop_id22*hitop_id6:1;User.Item*Item,hitop_id27*hitop_id6:1;User.phone*Item,device_name311*hitop_id6:1;User.pay*Item.price,pay_ability1*4593:1'],
    val data: RDD[Array[String]] = sc.textFile("000000_0").map(_.split("\t"))
    //得到第一列的值，也就是label  --[-1,1]
    val label: RDD[String] = data.map(_.take(1)(0))
    //格式化数据，用;做分隔符，分割之后是例如Item.id,hitop_id55:1
    //然后用:做分割符取第一个，也就是去掉了后面的:1 取出 Item.id,hitop_id55
    val sample: RDD[Array[String]] = data.map(_.drop(1)(0)).map(x=>{
      val arr: Array[String] = x.split(";").map(_.split(":")(0))
      arr
    })
    //将所有元素压平，得到的是所有分特征，然后去重，最后索引化，也就是加上下标，最后转成map是为了后面查询用 Item.id,hitop_id55 Item.screen,screen4
    val dict: Map[String, Long] = sample.flatMap(x=>{x}).distinct().zipWithIndex().collectAsMap()
    //得到稀疏向量
    val sam: RDD[SparseVector] = sample.map(sampleFeatures=>{
      //得到所有非零元素的下标，将样本中所有特征在字典中查询，查到的下标，就是非零元素的下标
      val index: Array[Int] = sampleFeatures.map(feature=>{
      //Item.id,hitop_id55
      //dict Item.id,hitop_id55:3
      // Item.id,hitop_id55,3 ,Item.id,hitop_id55,0
      //3,0 ,0,5
        //get出来的元素程序认定可能为空，做一个类型匹配
        val rs: Long =  dict.get(feature) match{
          case Some(x) => x
          case None => 0
        }
        //非零元素下标，转int符合SparseVector的构造函数
        rs.toInt
      })
      new SparseVector(dict.size,index,Array.fill(index.length)(1.0))
    })
    //举例zip用法
    //   val labelp: RDD[(Double, SparseVector)] = label.dict(x=>{
    //      x match{
    //        case "-1" => 0.0
    //        case "1" => 1.0
    //      }
    //    }).zip(sam)
    //mllib中的逻辑回归只认1.0和0.0，这里进行一个匹配转换
    val la: RDD[LabeledPoint] = label.map(x=>{
      x match{
        case "-1" => 0.0
        case "1" => 1.0
      }
      //标签组合向量得到labelPoint
    }).zip(sam).map(x=>new LabeledPoint(x._1,x._2))

//    MLUtils.saveLabeledData(la.sample(false,0.005),"trainSet")
//    MLUtils.saveLabeledData(la.sample(false,0.001),"testSet")
//    println("done")


    //逻辑回归训练，两个参数，迭代次数和步长，生产常用调整参数
     val lr = new LogisticRegressionWithSGD()
    // 设置W0截距
    lr.setIntercept(true)
    // 设置正则化
    lr.optimizer.setUpdater(new SquaredL2Updater)
    // 看中W模型推广能力的权重
    lr.optimizer.setRegParam(0.4)
    // 最大迭代次数
    lr.optimizer.setNumIterations(10)
    // 设置梯度下降的步长
    lr.optimizer.setStepSize(0.1)
    val model: LogisticRegressionModel = lr.run(la)

    //模型结果权重
    val weights: Array[Double] = model.weights.toArray
    //将map反转，weights相应下标的权重对应map里面相应下标的特征名
    val map: Map[Long, String] = dict.map(x=>(x._2,x._1))
    //模型保存
    //    LogisticRegressionModel.load()
    //    model.save()
    //输出
    val pw = new PrintWriter("result");
    //遍历
    for(i<- 0 until weights.length){
      //通过map得到每个下标相应的特征名
      val featureName = map.get(i)match {
        case Some(x) => x
        case None => ""
      }
      //特征名对应相应的权重
      val str = featureName+"\t" + weights(i)
      pw.write(str)
      pw.println()
    }
    pw.flush()
    pw.close()

  }
}