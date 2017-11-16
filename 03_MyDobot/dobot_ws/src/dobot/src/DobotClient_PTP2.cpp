/* ROS */
#include "ros/ros.h"
#include "std_msgs/String.h"
#include "dobot/SetPTPCmd.h"

/****** まとめ ******/
//main関数の中にすべて記載
// ノード作成する
// クライアントオブジェクトの変数宣言
// クライアントのノード作成
// クライアントのインスタンス生成 同時に、サーバに接続。
//　引数の宣言（SetPTPCmd型）
// 引数への値の代入

// 実際の作業：ループしながらサーバをコールする。変えるのは、ここだけか。。。
//　ここをサーバにすればよさげ。


int main(int argc, char **argv)
{

/****** 初期化宣言 ******/

	//ROSの初期化。DobotClientという名前のノードとして宣言する。
    ros::init(argc, argv, "DobotClient");

	//ノードハンドラの宣言。ノードの初期化処理を行う。
    ros::NodeHandle n;

	//クライアントの（戻り値の？）型
    ros::ServiceClient client;

	//クライアントインスタンス作成。つなげるサーバは："/DobotServer/SetPTPCmd"。　
    client = n.serviceClient<dobot::SetPTPCmd>("/DobotServer/SetPTPCmd");

	//SetPTPCmd（API関係）　の変数宣言。実体化しなくても、変数作れる？
    dobot::SetPTPCmd srv;

	
/****** 実行 ******/

	//Ctrl+Cが送られたりして、ros::ok()==falseになるまで繰り返す
    while (ros::ok()) {
				
        // 位置A
        do {
			//コールするための引数の設定
            srv.request.ptpMode = 1;
            srv.request.x = 200;
            srv.request.y = 0;
            srv.request.z = 0;
            srv.request.r = 0;
			
			//サーバをコール
            client.call(srv);
			
			//結果が来たら抜ける？0だからfalse??
            if (srv.response.result == 0) {
                break;
            }
			
			//ループ			
            ros::spinOnce();
			
			//異常があったら抜ける？
            if (ros::ok() == false) {
                break;
            }
        } while (1);


        // 位置B
        do {
            srv.request.ptpMode = 1;
            srv.request.x = 250;
            srv.request.y = 0;
            srv.request.z = 0;
            srv.request.r = 0;
            client.call(srv);
            if (srv.response.result == 0) {
                break;
            }
            ros::spinOnce();
            if (ros::ok() == false) {
                break;
            }
        } while (1);
  
        ros::spinOnce();
    }

    return 0;
}

