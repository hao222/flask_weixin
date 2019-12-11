//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        p:1,      // 当前页树
        processing:false     // 是否增加处理
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

    },
    // onShow 事件 每次进页面都需要加载新的数据
    onShow: function(){
        this.getBannerAndCat()
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
	listenerSearchInput:function( e ){
	        this.setData({
	            searchInput: e.detail.value
	        });
	 },
	 toSearch:function( e ){
	        this.setData({
	            p:1,
	            goods:[],
	            loadingMoreHidden:true
	        });
	        this.getFoodList();
	},
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },
    getBannerAndCat:function () {
        var that = this;
        wx.request({
            url: app.buildUrl("/food/index"),
            header: app.getRequestHeader(),
            success:function (res) {
                var resp = res.data;
                if (resp.code != 200){
                    app.alert({"content":resp.msg});
                    return;
                }
                that.setData({
                    banners: resp.data.banner_list,
                    categories: resp.data.cat_list
                });
                // 首页获取完之后也要进行一次查询
                that.getFoodList();
            }
        });
    },
    // 分类查询   需要初始化
    catClick:function(e){
        this.setData({
            activeCategoryId: e.currentTarget.id,  // 类别当前绑定对象
            p:1,
            goods:[],
            loadingMoreHidden:true
        });
        this.getFoodList();   //每次点击执行搜索事件
    },
    // 此方法是为了实现 分页效果  下拉请求  直接在js写就行 不需要调用
    onReachBottom:function(){
        var that = this;
        setTimeout(function () {
            that.getFoodList();
        }, 500);
    },
    getFoodList:function () {
        // 什么时候请求处理
        var that = this;
        if(that.data.processing == true){
            return;
        }
        if(!that.data.loadingMoreHidden){
            return;
        }
        // 正在请求
        that.setData({
            processing:true
        });
        wx.request({
            url: app.buildUrl("/food/search"),
            header: app.getRequestHeader(),
            data:{
                cat_id: that.data.activeCategoryId,
                mix_kw: that.data.searchInput,
                p: that.data.p
            },
            success:function (res) {
                var resp = res.data;
                if (resp.code != 200){
                    app.alert({"content":resp.msg});
                    return;
                }
                var goods = resp.data.list;
                that.setData({
                   goods:that.data.goods.concat(goods),      //  双向数据绑定 所以需要相加
                    p: that.data.p + 1,
                    processing: false      // 请求已完成  再次发送请求
                });
                if(resp.data.has_more == 0){
                    that.setData({
                        loadingMoreHidden:false
                    })
                }
            }
        });
    }

});
