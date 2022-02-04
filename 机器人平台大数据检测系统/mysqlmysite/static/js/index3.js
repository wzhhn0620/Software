// 柱状图1模块
(function() {
  // 实例化对象
  var myChart = echarts.init(document.querySelector(".bar .chart"));
  // 指定配置和数据
  // (1)准备数据
  var colors = ["#3794c0", "#cbebdb","#6dcc32","#aa04ae","#6dcc32","#F8B448","#c0175d","#7eff0a","#0fff06","#aea612","#42c00a"];
  var option = {
    color: colors,
    tooltip: {
      // 通过坐标轴来触发
      trigger: "axis"
    },
    // legend: {
    //   // 距离容器10%
    //   right: "10%",
    //   // 修饰图例文字的颜色
    //   textStyle: {
    //     color: "#4c9bfd"
    //   }
    //   // 如果series 里面设置了name，此时图例组件的data可以省略
    //   // data: ["邮件营销", "联盟广告"]
    // },
    grid: {
      top: "20%",
      left: "3%",
      right: "4%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true
    },

    xAxis: {
      type: "category",
      boundaryGap: false,
      data: xtime.xtemptime[0],
      // 去除刻度
      axisTick: {
        show: false
      },
      // 修饰刻度标签的颜色
      axisLabel: {
        color: "rgba(255,255,255,.7)"
      },
      // 去除x坐标轴的颜色
      axisLine: {
        show: false
      }
    },
    yAxis: {
      type: "value",
      // 去除刻度
      axisTick: {
        show: false
      },
      // 修饰刻度标签的颜色
      axisLabel: {
        color: "rgba(255,255,255,.7)"
      },
      // 修改y轴分割线的颜色
      splitLine: {
        lineStyle: {
          color: "#012f4a"
        }
      }
    },
    dataZoom: [{
            startValue: '0',
            show:false
        }, {
            type: 'inside'
    }],
    series: [
      {name: "机器人设备1",type: "line",smooth: true,data: data.year[0]},
      {name: "机器人设备2",type: "line",smooth: true,data: data.year[3]},
      {name: "机器人设备3",type: "line",smooth: true,data: data.year[6]},
      {name: "机器人设备4",type: "line",smooth: true,data: data.year[9]},
      {name: "机器人设备5",type: "line",smooth: true,data: data.year[12]},
      {name: "机器人设备6",type: "line",smooth: true,data: data.year[15]},
      {name: "机器人设备7",type: "line",smooth: true,data: data.year[18]},
      {name: "机器人设备8",type: "line",smooth: true,data: data.year[21]},
      {name: "机器人设备9",type: "line",smooth: true,data: data.year[24]},
      {name: "机器人设备10",type: "line",smooth: true,data: data.year[27]},
      {name: "机器人设备11",type: "line",smooth: true,data: data.year[30]},
    ]
  };

  // 3. 把配置和数据给实例对象
  myChart.setOption(option);

  // 重新把配置好的新数据给实例对象
  myChart.setOption(option);
  window.addEventListener("resize", function() {
    myChart.resize();
  });

})();

// 折线图定制
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".line .chart"));

  // (1)准备数据
  // var data = {
  //   year: [
  //     [24, 40, 101, 134, 90, 230, 210, 230, 120, 230, 210, 120],
  //     [40, 64, 191, 324, 290, 330, 310, 213, 180, 200, 180, 79]
  //   ]
  // };

  // 2. 指定配置和数据
  var option = {
    color: ["#3794c0", "#cbebdb","#6dcc32","#aa04ae","#6dcc32","#F8B448","#c0175d","#7eff0a","#0fff06","#aea612","#42c00a"],
    tooltip: {
      // 通过坐标轴来触发
      trigger: "axis"
    },
    // legend: {
    //   // 距离容器10%
    //   right: "10%",
    //   // 修饰图例文字的颜色
    //   textStyle: {
    //     color: "#4c9bfd"
    //   }
    //   // 如果series 里面设置了name，此时图例组件的data可以省略
    //   // data: ["邮件营销", "联盟广告"]
    // },
    grid: {
      top: "20%",
      left: "3%",
      right: "4%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true
    },

    xAxis:[
        {type: 'category', boundaryGap: false,axisTick: {alignWithLabel: true}, axisTick: {show: false},axisLabel: {color: "rgba(255,255,255,.7)"},data: xtime.xtemptime[0]},
        // {type: 'category', boundaryGap: false,axisTick: {alignWithLabel: true}, axisTick: {show: false},axisLabel: {color: "rgba(255,255,255,.7)"},data: xtime.xtemptime[1]},
    ],
    yAxis: {
      type: "value",
      // 去除刻度
      axisTick: {
        show: false
      },
      // 修饰刻度标签的颜色
      axisLabel: {
        color: "rgba(255,255,255,.7)"
      },
      // 修改y轴分割线的颜色
      splitLine: {
        lineStyle: {
          color: "#012f4a"
        }
      }
    },
    dataZoom: [{
            startValue: '0',
            show:false
        }, {
            type: 'inside'
    }],
    series: [
      {name: "机器人设备1",type: "line",smooth: true,data: data.year[1]},
      {name: "机器人设备2",type: "line",smooth: true,data: data.year[4]},
      {name: "机器人设备3",type: "line",smooth: true,data: data.year[7]},
      {name: "机器人设备4",type: "line",smooth: true,data: data.year[10]},
      {name: "机器人设备5",type: "line",smooth: true,data: data.year[13]},
      {name: "机器人设备6",type: "line",smooth: true,data: data.year[16]},
      {name: "机器人设备7",type: "line",smooth: true,data: data.year[19]},
      {name: "机器人设备8",type: "line",smooth: true,data: data.year[22]},
      {name: "机器人设备9",type: "line",smooth: true,data: data.year[25]},
      {name: "机器人设备10",type: "line",smooth: true,data: data.year[28]},
      {name: "机器人设备11",type: "line",smooth: true,data: data.year[31]},
    ]
  };
  // 3. 把配置和数据给实例对象
  myChart.setOption(option);

  // 重新把配置好的新数据给实例对象
  myChart.setOption(option);
  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();

// 饼形图定制
// 折线图定制
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".pie .chart"));

  option =  {
    color: ["#3794c0", "#cbebdb","#6dcc32","#aa04ae","#6dcc32","#F8B448","#c0175d","#7eff0a","#0fff06","#aea612","#42c00a"],
    tooltip: {
      // 通过坐标轴来触发
      trigger: "axis"
    },
    // legend: {
    //   // 距离容器10%
    //   right: "10%",
    //   // 修饰图例文字的颜色
    //   textStyle: {
    //     color: "#4c9bfd"
    //   }
    //   // 如果series 里面设置了name，此时图例组件的data可以省略
    //   // data: ["邮件营销", "联盟广告"]
    // },
    grid: {
      top: "20%",
      left: "3%",
      right: "4%",
      bottom: "3%",
      show: true,
      borderColor: "#012f4a",
      containLabel: true
    },

   xAxis:[
        {type: 'category',axisLine: {show: false}, boundaryGap: false,axisTick: {alignWithLabel: true}, axisTick: {show: false},axisLabel: {color: "rgba(255,255,255,.7)"},data: xtime.xtemptime[0]},
        // {type: 'category',axisLine: {show: false}, boundaryGap: false,axisTick: {alignWithLabel: true}, axisTick: {show: false},axisLabel: {color: "rgba(255,255,255,.7)"},data: xtime.xtemptime[1]},
    ],
    yAxis: {
      type: "value",
      // 去除刻度
      axisTick: {
        show: false
      },
      // 修饰刻度标签的颜色
      axisLabel: {
        color: "rgba(255,255,255,.7)"
      },
      // 修改y轴分割线的颜色
      splitLine: {
        lineStyle: {
          color: "#012f4a"
        }
      }
    },
    dataZoom: [{
            startValue: '0',
            show:false
        }, {
            type: 'inside'
    }],
    series: [
      {name: "机器人设备1",type: "line",smooth: true,data: data.year[2]},
      {name: "机器人设备2",type: "line",smooth: true,data: data.year[5]},
      {name: "机器人设备3",type: "line",smooth: true,data: data.year[8]},
      {name: "机器人设备4",type: "line",smooth: true,data: data.year[11]},
      {name: "机器人设备5",type: "line",smooth: true,data: data.year[14]},
      {name: "机器人设备6",type: "line",smooth: true,data: data.year[17]},
      {name: "机器人设备7",type: "line",smooth: true,data: data.year[20]},
      {name: "机器人设备8",type: "line",smooth: true,data: data.year[23]},
      {name: "机器人设备9",type: "line",smooth: true,data: data.year[26]},
      {name: "机器人设备10",type: "line",smooth: true,data: data.year[29]},
      {name: "机器人设备11",type: "line",smooth: true,data: data.year[32]},
    ]
  };

  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();
// 学习进度柱状图模块
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".bar1 .chart"));

  var option = {
    legend: {
      top: "90%",
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        color: "rgba(255,255,255,.5)",
        fontSize: "12"
      }
    },
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    // 注意颜色写的位置
    color: [
      "#006cff",
      "#60cda0",
      "#ed8884",
      "#ff9f7f",
      "#0096ff",
      "#9fe6b8",
      // "#32c5e9",
      // "#1d9dff"
    ],
    series: [
      {
        name: "点位统计",
        type: "pie",
        // 如果radius是百分比则必须加引号
        radius: ["10%", "70%"],
        center: ["50%", "42%"],
        roseType: "radius",
        data: [
          { value: 30, name: "root用户" },
          { value: 26, name: "har用户" },
          { value: 24, name: "zy用户" },
          { value: 25, name: "clh用户" },
          { value: 20, name: "wfl用户" },
          { value: 25, name: "gsm用户" },
          // { value: 30, name: "深圳" },
          // { value: 42, name: "广东" }
        ],
        // 修饰饼形图文字相关的样式 label对象
        label: {
          fontSize: 10
        },
        // 修饰引导线样式
        labelLine: {
          // 连接到图形的线长度
          length: 10,
          // 连接到文字的线长度
          length2: 10
        }
      }
    ]
  };

  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();
// 折线图 优秀作品
(function() {
  // 基于准备好的dom，初始化echarts实例
  var myChart = echarts.init(document.querySelector(".line1 .chart"));

 option = {
       color: [
      "#006cff",
      "#60cda0",
      "#ed8884",
      // "#ff9f7f",
      // "#0096ff",
      // "#9fe6b8",
      // "#32c5e9",
      // "#1d9dff"
    ],
    tooltip: {
        trigger: 'item'
    },
    legend: {
        top: '90%',
        left: 'center',
        textStyle: {
        color: "rgba(255,255,255,.5)",
        fontSize: "12"
      }
    },
    series: [
        {
            name: '访问来源',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
                borderRadius: 10,
                borderColor: '#fff',
                borderWidth: 2
            },
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '15',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: [
                {value: 1048, name: '机器人wzh'},
                {value: 735, name: '机器人wrd'},
                {value: 580, name: '机器人wy'}
                // {value: 484, name: '联盟广告'},
                // {value: 300, name: '视频广告'}
            ]
        }
    ]
};

  // 使用刚指定的配置项和数据显示图表。
  myChart.setOption(option);
  window.addEventListener("resize", function() {
    myChart.resize();
  });
})();

// 点位分布统计模块
(function() {
  // 1. 实例化对象
  var myChart = echarts.init(document.querySelector(".pie1  .chart"));
  // 2. 指定配置项和数据
  var option = {
    legend: {
      top: "90%",
      itemWidth: 10,
      itemHeight: 10,
      textStyle: {
        color: "rgba(255,255,255,.5)",
        fontSize: "12"
      }
    },
    tooltip: {
      trigger: "item",
      formatter: "{a} <br/>{b} : {c} ({d}%)"
    },
    // 注意颜色写的位置
    color: [
      "#006cff",
      "#60cda0",
      "#ed8884",
      "#ff9f7f",
      "#0096ff",
      "#9fe6b8",
      "#32c5e9",
      "#1d9dff"
    ],
    series: [
      {
        name: "点位统计",
        type: "pie",
        // 如果radius是百分比则必须加引号
        radius: ["10%", "70%"],
        center: ["50%", "42%"],
        roseType: "radius",
        data: [
          { value: 20, name: "云南" },
          { value: 26, name: "北京" },
          { value: 24, name: "山东" },
          { value: 25, name: "河北" },
          { value: 20, name: "江苏" },
          { value: 25, name: "浙江" },
          { value: 30, name: "深圳" },
          { value: 42, name: "广东" }
        ],
        // 修饰饼形图文字相关的样式 label对象
        label: {
          fontSize: 10
        },
        // 修饰引导线样式
        labelLine: {
          // 连接到图形的线长度
          length: 10,
          // 连接到文字的线长度
          length2: 10
        }
      }
    ]
  };

  // 3. 配置项和数据给我们的实例化对象
  myChart.setOption(option);
  // 4. 当我们浏览器缩放的时候，图表也等比例缩放
  window.addEventListener("resize", function() {
    // 让我们的图表调用 resize这个方法
    myChart.resize();
  });
})();
