require('!!file-loader?name=[name].[ext]!./index.html')


var When = require('when')
/* required library for our React app */
var ReactDOM = require('react-dom')
var React = require("react")
var Qs = require('qs')
var Cookie = require('cookie')
var createReactClass = require('create-react-class')

var API = require("./utils/api")

/* required css for our application */
require('./webflow/css/style.css');

var ResearchModal = require("./components/research_modal")
var Map = require("./components/map")

const Home = createReactClass({
    getInitialState() {
      return {
        modal: false,
      }
    },
    launchResearch(value){
      if (!value)
        return;
      console.log("reseach data");
      console.log(value);
      API.query_map(value["interest"],
        value["lat"], value["long"], value["start"], value["end"]).then((data) => {
          this.setState({
            remoteData: data
          })
        })
    },
    render(){
      var props = {
        ...this.props,
        callback: (value) => {
          this.setState({modal: false})
          this.launchResearch(value);
        },
        remoteData: this.state.remoteData
      }

      var modal_content = <ResearchModal {...props} />

      var hidden_modal = this.state.modal ? "hidden" : "";

      var map = <Map {...props} />

      return <JSXZ in="index" sel=".layout">
        <Z sel=".center .map">
          {map}
        </Z>
        <Z sel=".right-col .interest-infos-header">
          <ChildrenZ/>
        </Z>
        <Z sel=".right-col .infos-list">
          <ChildrenZ/>
        </Z>
        <Z sel=".right-col .research-infos .research-button" onClick={(e) => {
            this.setState({modal: true})
        }}>
          <ChildrenZ/>
        </Z>
        <Z sel=".modal-wrapper" className={classNameZ + hidden_modal}>
          {modal_content}
        </Z>
      </JSXZ>
    }
  })

ReactDOM.render(<Home/>, document.getElementById('root'))