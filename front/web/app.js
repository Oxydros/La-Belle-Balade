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

const ResearchModal = createReactClass({
  getInitialState(){
    return {}
  },
  getHourArray() {
    var arr = [], i, j;
    for(i=0; i<24; i++) {
      for(j=0; j<4; j++) {
        arr.push(i + ":" + (j===0 ? "00" : 15*j) );
      }
    }
    return arr;
  },
  render(){
    return <JSXZ in="index" sel=".research-modal">
      <Z sel=".research-header"><ChildrenZ/></Z>
      <Z sel=".research-interests .select-interests" multiple={true} onChange={(e) => {
        var selectedValues = Array.from(e.target)
        .map(option => option.value)
        this.setState({interest: selectedValues})
      }}><ChildrenZ/></Z>
      <Z sel=".research-hours .start-hour" onChange={(e) => {
        this.setState({start: e.target.value})
      }}>
      {
        this.getHourArray().map((hour) => {
          return <option value={hour}>{hour}</option>
        })
      }
      </Z>
      <Z sel=".research-hours .end-hour" onChange={(e) => {
        this.setState({end: e.target.value})
      }}>
            {
        this.getHourArray().map((hour) => {
          return <option value={hour}>{hour}</option>
        })
      }
      </Z>
      <Z sel=".research-pos .lat-input" onChange={(e) => {
        this.setState({lat: e.target.value})
      }}><ChildrenZ/></Z>
      <Z sel=".research-pos .long-input" onChange={(e) => {
        this.setState({long: e.target.value})
      }}><ChildrenZ/></Z>

      <Z sel=".research-submit .ok-button" onClick={(e) => {
        e.preventDefault()

        this.props.callback(this.state);
      }}><ChildrenZ/></Z>

      <Z sel=".research-submit .ko-button" onClick={(e) => {
        e.preventDefault()
        this.props.callback(false);
      }}><ChildrenZ/></Z>
    </JSXZ>
  }
})

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
        value["lat"], value["long"], value["start"], value["end"])
    },
    render(){

      var props = {
        ...this.props,
        callback: (value) => {
          this.setState({modal: false})
          this.launchResearch(value);
        }
      }

      var modal_content = <ResearchModal {...props} />

      var hidden_modal = this.state.modal ? "hidden" : "";

      return <JSXZ in="index" sel=".layout">
        <Z sel=".center">
          <ChildrenZ/>
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