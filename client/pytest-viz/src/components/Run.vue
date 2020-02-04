<template>

  <v-container>
    <v-app-bar dark fixed dense>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Available Tests</v-toolbar-title>
      <div class="text-center">
        <v-btn v-if="autoTests === 'path'" class="ma-2" tile color="orange" light @click="collectTestPaths()">Collect</v-btn>
        <v-btn v-else class="ma-2" tile color="orange" light @click="collectTests()">Collect</v-btn>
        <v-avatar v-if="collectedTestsCount" color="orange" size="35">
          <span class="white--text headline">{{collectedTestsCount}}</span>
        </v-avatar>
        <template v-if="nothingSelected(selection)">
            <v-btn class="ma-2" tile color="blue" @click="runAllTests()">Run All</v-btn>
        </template>
        <template v-else>
          <template v-if="autoTests === 'path'">
            <v-btn class="ma-2" tile color="blue" @click="runSelectedPaths()">Run Paths</v-btn>
          </template>
          <template v-else>
            <v-btn class="ma-2" tile color="blue" @click="runSelectedTests()">Run Selected</v-btn>
          </template>
        </template>
        <v-avatar v-if="executedTestsCount" color="blue" size="35">
          <span class="white--text headline">{{executedTestsCount}}</span>
        </v-avatar>
        <v-avatar v-if="failedTests.length > 0" color="red" size="35">
          <span class="white--text headline">{{failedTests.length}}</span>
        </v-avatar>
      </div>
    </v-app-bar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
    >
      <v-subheader>Config</v-subheader>
      <v-list-item nav>
        <v-switch
          v-model="auto"
          class="ma-2"
          label="Auto"
          @change="saveAutoConfig()"
        ></v-switch>
      </v-list-item>
      <v-list-item nav>
        <v-radio-group v-model="autoTests" @change="saveAutoTestsConfig()">
          <v-radio v-if="auto" value="failed" label="Failed Tests"></v-radio>
          <v-radio v-if="auto" value="all" label="All Tests"></v-radio>
          <v-radio v-if="auto" value="selected" label="Only Selected Ones"></v-radio>
          <v-radio v-if="auto" value="path" label="All Tests Within Selected Path(s)"></v-radio>
        </v-radio-group>
      </v-list-item>
    </v-navigation-drawer>

    <v-row no-gutters>
      <v-col
        cols="12"
        sm="4"
      >
        <v-card
          class="pa-2"
          outlined
          tile
        >
        </v-card>
      </v-col>
    </v-row>

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
        <template v-if="!collectedTests.length && !collectedPaths.length">
          Collect tests to see them here!
        </template>
        <template v-if="autoTests === 'path'">
          <v-treeview
            v-model="selection"
            :items="collectedPaths"
            item-key="id"
            selectable
            return-object
            open-on-click
            item-disabled="isSingleTest"
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
              <v-icon v-else>
                {{ 'mdi-flash-outline' }}
              </v-icon>
            </template>
          </v-treeview>
        </template>
        <template v-else>
          <v-treeview
            v-model="selection"
            :items="collectedTests"
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
        <template v-if="!executedTests.length">
          Run some tests to see the results here!
        </template>
        <template v-else>
          <v-treeview
            :items="executedTests"
            item-key="id"
            activatable
            :active="active"
            return-object
            @update:active="showErrorDialog"
            :open.sync="open"
            open-on-click
            open-all
            dense
          >
            <template v-slot:append="{item}">
              <!-- <v-btn v-if="!item.passed && item.wasExecuted">Show Error</v-btn> -->
              <v-alert text dense outlined v-if="!item.passed && item.wasExecuted" type="error">
                <pre>{{item.errorRepr}}</pre>
              </v-alert>
            </template>
            <template v-slot:prepend="{ item, open }">
              <v-icon color="red" v-if="item.isPackage && item.containsFailedTests">
                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
              </v-icon>
              <v-icon color="green" v-if="item.isPackage && !item.containsFailedTests">
                {{ open ? 'mdi-folder-open' : 'mdi-folder' }}
              </v-icon>
              <v-icon color="red" v-else-if="item.isModule && item.containsFailedTests">
                {{ 'mdi-language-python' }}
              </v-icon>
              <v-icon color="green" v-else-if="item.isModule && !item.containsFailedTests">
                {{ 'mdi-language-python' }}
              </v-icon>
              <v-icon color="red" v-else-if="item.isKlass && item.containsFailedTests">
                {{ 'mdi-file-table-box-multiple-outline' }}
              </v-icon>
              <v-icon color="green" v-else-if="item.isKlass && !item.containsFailedTests">
                {{ 'mdi-file-table-box-multiple-outline' }}
              </v-icon>
              <v-icon color="green" v-else-if="item.wasExecuted && item.passed">
                {{ 'mdi-check-bold' }}
              </v-icon>
              <v-icon color="red" v-else-if="item.wasExecuted && !item.passed">
                {{ 'mdi-exclamation-thick' }}
              </v-icon>
            </template>
          </v-treeview>
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

    <v-alert v-if="alert" dense prominent type="warning">
      Detected changes to tests, so I had to <b>Collect</b> again.
    </v-alert>

    <template  v-if="userCodeFailure">
      <v-alert dense prominent type="error">
        Cannot collect or run tests! See below.
      </v-alert>
      <v-divider></v-divider>
      <v-sheet 
        color="black lighten-2" 
        dark
        >
        <pre>{{userCodeFailure}}</pre>
      </v-sheet>
    </template>
  </v-container>

</template>

<script>
import ApiService from "@/services/ApiService";
import Test from "@/models/Test";
import Config from "@/models/Config";

let syncer = new Test.Synchronizer();

export default {
  name: "Run",

  data: () => ({
    collectedTests: [],
    collectedPaths: [],
    selection: [],
    executedTests: [],
    active: [],
    dialog: false,
    error: null,
    panel: 0,  // always open the first panel only
    failedTests: [],
    testExecutionInProgress: false,
    testCollectionInProgress: false,
    userCodeFailure: null,
    open: [],
    drawer: null,
    auto: Config.getAuto(),
    autoTests: Config.getAutoTests(),
    collectedTestsCount: null,
    executedTestsCount: null,
    alert: null,
  }),
  methods: {
    async collectTests () {
      syncer.collectTests(this);
    },
    async collectTestPaths(){
      syncer.collectPaths(this);
    },
    async runAllTests () {
      syncer.runAllTests(this);
    },
    async runSelectedTests () {
      syncer.runSelectedTests(this);
    },
    async runSelectedPaths() {
      if (!this.collectedPaths){
        syncer.collectPaths(this);
      }
      syncer.runTestsInPaths(this);
    },
    async runFailedTests(){
      syncer.runFailedTests(this);
    },
    nothingSelected (selection) {
      if (this.autoTests === 'path'){
        var selectedTests = selection;
      }
      else{
        var selectedTests = Test.getTestCasesOnly(selection);
      }

      return selectedTests.length < 1;
    },
    showErrorDialog (selected) {
      if (selected.length) {
        this.error = selected[0].errorRepr;
        this.dialog = true;
      }
    },
    saveAutoConfig (){
      Config.saveAutoConfig(this);
    },
    saveAutoTestsConfig(){
      Config.saveAutoTestsConfig(this);
    }
  },
  watch : {
    autoTests: function (val){
      if (val === 'path'){
        syncer.collectPaths(this);
      }
      else{
        syncer.resetCollectedPaths(this);
      }
    }
  },
  sockets: {
    connect: function () {
      console.log('socket connected to backend');
      if (localStorage.getItem('auto') === 'true'){  // Config.getAuto()
        if (localStorage.getItem('autoTests') === 'failed'){  //Config.getAutoTests()
          this.runFailedTests();
        }
        else if (localStorage.getItem('autoTests') === 'all'){  //Config.getAutoTests()
          this.runAllTests();
        }
        else if (localStorage.getItem('autoTests') === 'selected'){  //Config.getAutoTests()
          this.runSelectedTests();
        }
      }
    },
  },
};
</script>
