module.exports = {
    devServer: {
        host: '0.0.0.0',
        disableHostCheck: true
    },
    css: {
        loaderOptions: {
            sass: {
                prependData: `@import "@/assets/styles/_app.scss";`
            },
            scss: {
                prependData: `@import "@/assets/styles/_app.scss";`
            }
        }
    }
}