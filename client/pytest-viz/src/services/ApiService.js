import Api from '@/services/Api'

export default {
    runTests () {
        return Api().get('tests/run');
    },
    collectTests () {
        return Api().get('tests');
    },
    RunSelectedTests (nodeIDs) {
        return Api().post(`tests/run`, nodeIDs);
    }
}
