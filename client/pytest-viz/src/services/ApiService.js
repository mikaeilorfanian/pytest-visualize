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
    runTestsForPaths (paths) {
        console.log(paths);
        const pathsArr = Array.from(paths, pathObj => pathObj.id);
        return Api().get('executed_tests', {params: {'paths': JSON.stringify(pathsArr)}});
    },
    collectTestsPaths (){
        return Api().get('collected_tests?paths=.');
    }
}
