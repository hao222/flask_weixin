//index.js
//获取应用实例
var app = getApp();
var WxParse = require('../../wxParse/wxParse.js');
// 加载 utils.js
var utils = require('../../utils/util.js');


Page({
    data: {
        autoplay: true,
        interval: 3000,
        duration: 1000,
        swiperCurrent: 0,
        hideShopPopup: true,
        buyNumber: 1,
        buyNumMin: 1,
        buyNumMax:1,
        canSubmit: false, //  选中时候是否允许加入购物车
        shopCarInfo: {},
        shopType: "addShopCar",//购物类型，加入购物车或立即购买，默认为加入购物车,
        id: 0,
        shopCarNum: 0,
        commentCount:2
    },
    onLoad: function (e) {
        var that = this;
        that.setData({
            id:e.id
        });
    },
    onShow:function(){
        // 调取详情方法
        this.getInfo();
    },
    goShopCar: function () {
        wx.reLaunch({
            url: "/pages/cart/index"
        });
    },
    toAddShopCar: function () {
        this.setData({
            shopType: "addShopCar"
        });
        this.bindGuiGeTap();
    },
    tobuy: function () {
        this.setData({
            shopType: "tobuy"
        });
        this.bindGuiGeTap();
    },
    // 添加购物车
    addShopCar: function () {
        var that = this;
        var data = {
            "id": this.data.info.id,
            "number": this.data.buyNumber
        };
        wx.request({
            url: app.buildUrl("/cart/set"),
            header: app.getRequestHeader(),
            data:data,
            method:"POST",
            success:function (res) {
                var resp = res.data;
                app.alert({"content": resp.msg});
                that.setData({
                    // 加入成功后 让页面返回原来的
                    hideShopPopup: true
                });
                that.onShow();
            }
        });

    },
    // 立即购买
    buyNow: function () {
        var that = this;
        var data = {
            goods:[{
                "id":this.data.info.id,
                "price":this.data.info.price,
                "number":this.data.buyNumber,
            }]
        };
        that.setData({
            // 加入成功后 让页面返回原来的
            hideShopPopup: true
        });
        // 页面跳转 页面之间跳转传参数
        wx.navigateTo({
            url: "/pages/order/index?data" + JSON.stringify(data)
        });
    },
    /**
     * 规格选择弹出框
     */
    bindGuiGeTap: function () {
        this.setData({
            hideShopPopup: false
        })
    },
    /**
     * 规格选择弹出框隐藏
     */
    closePopupTap: function () {
        this.setData({
            hideShopPopup: true
        })
    },
    numJianTap: function () {
        if( this.data.buyNumber <= this.data.buyNumMin){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum--;
        this.setData({
            buyNumber: currentNum
        });
    },
    numJiaTap: function () {
        if( this.data.buyNumber >= this.data.buyNumMax ){
            return;
        }
        var currentNum = this.data.buyNumber;
        currentNum++;
        this.setData({
            buyNumber: currentNum
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    getInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/food/info"),
            header: app.getRequestHeader(),
            data:{
                id: that.data.id
            },
            success:function (res) {
                var resp = res.data;
                if (resp.code != 200) {
                    app.alert({"content": resp.msg});
                    return;
                }
                that.setData({
                    info: resp.data.info,
                    buyNumMax: resp.data.info.stock,
                    shopCarNum: resp.data.cart_number
                });
                // 解析HTML内容 一般 富文本编辑器
                WxParse.wxParse('article', 'html', that.data.info.summary, that, 5);
            }
        });
    },
    // 实现转发功能
    onShareAppMessage: function () {
        var that = this;
        return {
            title: that.data.info.name,
            path: '/pages/food/info?id=' + that.data.info.id,
            success:function (res) {
                // 最新小程序转发接口没有此分析成功后的回调了
                // 转发成功 需要将请求数据发送到后端
                wx.request({
                    url:app.buildUrl("/member/share"),
                    header:app.getRequestHeader(),
                    method:"POST",
                    data:{
                        url: utils.getCurrentPageUrlWithArgs()
                    },
                    success:function (res) {

                    }
                });
            },

            fail: function (res) {

            }
    }
    }
});
