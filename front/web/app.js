require('!!file-loader?name=[name].[ext]!./index.html')


var When = require('when')
/* required library for our React app */
var ReactDOM = require('react-dom')
var React = require("react")
var Qs = require('qs')
var Cookie = require('cookie')
var createReactClass = require('create-react-class')

var API = require("./utils/api")

Number.prototype.toHHMMSS = function () {
  var seconds = Math.floor(this),
      hours = Math.floor(seconds / 3600);
  seconds -= hours*3600;
  var minutes = Math.floor(seconds / 60);
  seconds -= minutes*60;

  if (hours   < 10) {hours   = "0"+hours;}
  if (minutes < 10) {minutes = "0"+minutes;}
  if (seconds < 10) {seconds = "0"+seconds;}
  return hours+':'+minutes+':'+seconds;
}

/* required css for our application */
require('./webflow/css/style.css');

var ResearchModal = require("./components/research_modal")
var Map = require("./components/map")

const Infos = createReactClass({
    getInitialState() {
      return {
        modal: false,
      }
    },
    launchResearch(data){
      if (!data)
        return;

      API.query_map({...data, long: document.getElementById("long").value, lat: document.getElementById("lat").value}).then((data) => {
          this.props.updateData(data)
          // this.setState({
          //   remoteData: data
          // })
        })
    },
    render(){
      var props = {
        ...this.props,
        callback: (value) => {
          this.setState({modal: false})
          this.launchResearch(value);
        },
      }

      var modal_content = <ResearchModal {...props} />

      var hidden_modal = this.state.modal ? "" : " hidden";

      var schedule = this.props.data && this.props.data.schedule || []

      return <JSXZ in="index" sel=".right-col">
        <Z sel=".interest-infos-header">
          <ChildrenZ/>
        </Z>
        <Z sel=".infos-list">
          {
            schedule.map((schedule, i) => {
              var arrival = new Date(null);
              arrival.setSeconds(schedule[0]); // specify value for SECONDS here
              var timeStringArrival = arrival.toISOString().substr(11, 8);

              return <JSXZ in="index" sel=".infos-box" key={"schedule"+i}>
                <Z sel=".info-number">{i+1}</Z>
                <Z sel=".int-name">{this.props.data.coord[i + 1][0]}</Z>
                <Z sel=".int-type">TODO TYPE</Z>
                <Z sel=".int-arrival-time">Arrival time: {schedule[0].toHHMMSS()}</Z>
                <Z sel=".int-visit-time">Visit time: {schedule[1].toHHMMSS()}</Z>
              </JSXZ>
            })
          }
        </Z>

        <Z sel=".research-infos .research-button" onClick={(e) => {
            this.setState({modal: true})
        }}>
          <ChildrenZ/>
        </Z>

        <Z sel=".research-infos .lat-input" id="lat">
          <ChildrenZ/>
        </Z>

        <Z sel=".research-infos .long-input" id="long">
          <ChildrenZ/>
        </Z>        

        <Z sel=".modal-wrapper" className={classNameZ + hidden_modal}>
          {modal_content}
        </Z>
      </JSXZ>
    }
  })

  const Home = createReactClass({
    getInitialState(){
      return {
        data: {}
      }
    },
    updateData(data){
      this.setState({
        data: data
      })
    },
    render(){
      var props = {
        ...this.props,
        updateData: this.updateData,
        data: this.state.data
      }

      return <JSXZ in="index" sel=".layout">
          <Z sel=".layout-container">
            {<Map {...props}/>}
            {<Infos {...props} />}
          </Z>
        </JSXZ>
    }
  })

ReactDOM.render(<Home/>, document.getElementById('root'))