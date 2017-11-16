//
#include "ros/ros.h"
#include "stdio.h"
#include "std_msgs/String.h"
#include "std_msgs/Float32MultiArray.h"
#include "DobotDll.h"
#include "time.h"

/****** まとめ ******/
//main関数が呼ばれる
//main関数は、InitPTPService関数を呼ぶ
//InitPTPService関数は、
  //サーバノード作成
  //サーバのインスタンス生成。同時に、コールバック関数として、SetPTPCmdService関数を登録する。
//SetPTPCmdService関数は、実際の処理内容を記載。APIの、SetPTP関数を呼ぶ。




/*--- test用xミリ秒経過するのを待つ ---*/

int sleepa(unsigned long x)
{
    clock_t  s = clock();
    clock_t  c;

    do {
        if ((c = clock()) == (clock_t)-1)       /* エラー */
            return (0);
    } while (1000UL * (c - s) / CLOCKS_PER_SEC <= x); 
    return (1);
}



/****** サーバから呼ばれるコールバック関数：実際の処理 ******/
#include "dobot/SetPTPCmd.h"

//Requestと、Responseが引数
bool SetPTPCmdService(dobot::SetPTPCmd::Request &req, dobot::SetPTPCmd::Response &res)
{
    int code;
    PTPCmd cmd;
    uint64_t queuedCmdIndex;

    cmd.ptpMode = req.ptpMode;
    cmd.x = req.x; //Request型から、PTPCmd型に値を移し替える？
    cmd.y = req.y;
    cmd.z = req.z;
    cmd.r = req.r;
	
	//APIのSetPTPCmdを呼ぶ。結果は
    //res.result = SetPTPCmd(&cmd, true, &queuedCmdIndex);
	
	//test用
    code = sleepa(1000);
	ROS_INFO_STREAM("Hello World!"); 
	res.result = 0;
    

	//SetPTPCmd
	/*
		uint8 ptpMode
		float32 x
		float32 y
		float32 z
		float32 r
		---
		int32 result
		uint64 queuedCmdIndex
	*/
	
    return true;
}


/****** サーバ関数 ******/
void InitPTPServices(ros::NodeHandle &n, std::vector<ros::ServiceServer> &serverVec)
{
	//サーバの（戻り値の？）型
    ros::ServiceServer server;

	//サーバインスタンス作成。名前："/DobotServer/SetPTPCmd"。　コールバックする関数：SetPTPCmdSerVice
    server = n.advertiseService("/DobotServer/SetPTPCmd", SetPTPCmdService);

	//?
    serverVec.push_back(server);
}


/****** main関数 ******/

int main(int argc, char **argv)
{
	
	//ノード作成。名前は、"DobotServer"
    ros::init(argc, argv, "DobotServer");

	//ノードハンドラ。なにこれ？
    ros::NodeHandle n;

	//サーバー番号？
    std::vector<ros::ServiceServer> serverVec;

	//サーバープログラム実行
    InitPTPServices(n, serverVec);

	//終了するまでループ
    ros::spin();

    // Disconnect Dobot
    DisconnectDobot();

    return 0;
}

