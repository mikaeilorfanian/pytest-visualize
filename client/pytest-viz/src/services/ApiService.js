import Api from '@/services/Api'

export default {
    runTests () {
        return Api().get('tests/run');
    },
    collectTests () {
        return Api().get('tests');
    },
    runSelectedTests (nodeIDs) {
        return Api().post(`tests/run`, nodeIDs);
    },
    collectTestsPaths (){
        return Api().get('collected_tests?paths=.');
    }
}
