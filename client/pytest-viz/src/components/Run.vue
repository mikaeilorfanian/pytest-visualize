<template>

  <v-container>
    <v-toolbar color="teal" dark>
      <v-toolbar-title>Tests</v-toolbar-title>
      <div class="text-center">
        <v-btn class="ma-2" tile color="orange" light @click="collectTests()">Collect</v-btn>
        <template v-if="nothingSelected(selection)">
            <v-btn class="ma-2" tile color="green" @click="RunAllTests()">Run All</v-btn>
        </template>
        <template v-else>
            <v-btn class="ma-2" tile color="green" @click="RunSelectedTests()">Run Selected</v-btn>
        </template>
      </div>
    </v-toolbar>

    <v-row>
      <v-col class="pa-6">
        <template v-if="testCollectionInProgress">
          <div class="text-center">
            <v-progress-circular
              :size="70"
              :width="7"
              color="orange"
              indeterminate
            ></v-progress-circular>
          </div>
        </template>
        <template v-if="!collected_tests.length">
          Collect tests to see them here!
        </template>
        <template v-else>
          <v-treeview
            v-model="selection"
            :items="collected_tests"
            item-key="id"
            selectable
            return-object
            open-on-click
          >
            <template v-slot:prepend="{ item, open }">
              <v-icon v-if="item.isPackage">
                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
              </v-icon>
              <v-icon v-else-if="item.isModule">
                {{ 'mdi-language-python' }}
              </v-icon>
              <v-icon v-else-if="item.isKlass">
                {{ 'mdi-file-table-box-multiple-outline' }}
              </v-icon>
              <v-icon color="green" v-else-if="item.wasExecuted && item.passed">
                {{ 'mdi-flash' }}
              </v-icon>
              <v-icon color="red" v-else-if="item.testRan && !item.passed">
                {{ 'mdi-flash' }}
              </v-icon>
              <v-icon v-else>
                {{ 'mdi-flash-outline' }}
              </v-icon>
            </template>
          </v-treeview>
        </template>
      </v-col>

      <v-divider vertical></v-divider>

      <v-col class="pa-6" cols="6">
        <template v-if="testExecutionInProgress">
          <div class="text-center">
            <v-progress-circular
              :size="70"
              :width="7"
              color="green"
              indeterminate
            ></v-progress-circular>
          </div>
        </template>
        <template v-if="!executed_tests.length">
          <!-- <template v-if="errorMsg">{{errorMsg}}</template> -->
          Run some tests to see the results here!
        </template>
        <template v-else>
          <v-treeview
            open-all
            :items="executed_tests"
            item-key="id"
            activatable
            :active="active"
            return-object
            @update:active="showErrorDialog"
          >
            <template v-slot:prepend="{ item, open }">
              <v-icon v-if="item.isPackage">
                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
              </v-icon>
              <v-icon v-else-if="item.isModule">
                {{ 'mdi-language-python' }}
              </v-icon>
              <v-icon v-else-if="item.isKlass">
                {{ 'mdi-file-table-box-multiple-outline' }}
              </v-icon>
              <v-icon color="green" v-else-if="item.wasExecuted && item.passed">
                {{ 'mdi-flash' }}
              </v-icon>
              <v-icon color="red" v-else-if="item.testRan && !item.passed">
                {{ 'mdi-flash' }}
              </v-icon>
              <v-icon v-else>
                {{ 'mdi-flash-outline' }}
              </v-icon>
            </template>
          </v-treeview>
            <!-- {{ node.name }} -->
        </template>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" width="600px">
      <v-card>
        <v-card-title>
          <span class="headline">Error details</span>
        </v-card-title>
        <v-card-text v-model="error"><pre>{{error}}</pre></v-card-text>
      </v-card>
    </v-dialog>

    <!-- <v-expansion-panels>
      <v-expansion-panel
        v-model="panel"
        v-for="(test) in failedTests"
        :key="test.id"
      >
        <v-expansion-panel-header>{{test.id}}</v-expansion-panel-header>
        <v-expansion-panel-content>
          <pre>{{test.errorRepr}}</pre>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels> -->

    <v-sheet 
      color="black lighten-2" 
      v-model="panel"
      v-for="(test) in failedTests"
      :key="test.id"
      dark
      >
      <pre>{{test.errorRepr}}</pre>
    </v-sheet>
  </v-container>

</template>

<script>
import ApiService from "@/services/ApiService";
import Test from "@/models/Test";

export default {
  name: "Run",

  data: () => ({
    collected_tests: [],
    selection: [],
    executed_tests: [],
    active: [],
    dialog: false,
    error: null,
    panel: 0,  // always open the first panel only
    failedTests: [],
    testExecutionInProgress: false,
    testCollectionInProgress: false,
  }),

  // async mounted() {
  //   const resp = await ApiService.collectTests();
  //   this.tests = resp.data.tests;
  // },

  methods: {
    async collectTests () {
      let syncer = new Test.Synchronizer(this);
      syncer.collectTests();
    },
    async RunAllTests () {
      let syncer = new Test.Synchronizer(this);
      syncer.runAllTests();
    },
    async RunSelectedTests () {
      let syncer = new Test.Synchronizer(this);
      syncer.runSelectedTests();
    },
    nothingSelected (selection) {
        const selectedTests = Test.filterOutTestModules(selection);
        return selectedTests.length < 1;
    },
    showErrorDialog (selected) {
      if (selected.length) {
        this.error = selected[0].errorRepr;
        this.dialog = true;
      }
      
    }
  },

  sockets: {
        connect: function () {
            console.log('socket connected to backend');
            if (this.nothingSelected(this.selection)) {
              // this.collectTests();
              // this.selection = this.collected_tests;
              // this.RunAllTests();
            }
            else {
              this.RunSelectedTests();
            }
        },
        // customEmit: function (data) {
        //     console.log('this method was fired by the socket server. eg: io.emit("customEmit", data)')
        // }
    },
    // methods: {
    //     clickButton: function (data) {
    //         // $socket is socket.io-client instance
    //         this.$socket.emit('emit_method', data)
    //     }
    // }
};
</script>
