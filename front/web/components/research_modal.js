var React = require("react")
var createReactClass = require('create-react-class')

var API = require("../utils/api")

var interests_name = ["museum", "parc"]
var interests_values = [0, 0.5, 1]

module.exports = createReactClass({
  getInitialState(){
    return {
    }
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

  // onChange={(e) => {
  //   var selectedValues = Array.from(e.target)
  //   .map(option => option.value)
  //   this.setState({interest: selectedValues})
  // }}

  render(){
    return <JSXZ in="index" sel=".research-modal">
      <Z sel=".research-header"><ChildrenZ/></Z>

      <Z sel=".research-interests .interest-museum .interest-value" onChange={(e) => {
        this.setState({museum: e.target.value})
      }}><ChildrenZ/></Z>
      
      <Z sel=".research-interests .interest-parc .interest-value" onChange={(e) => {
        this.setState({parc: e.target.value})
      }}><ChildrenZ/></Z>

      <Z sel=".research-interests .interest-art .interest-value" onChange={(e) => {
        this.setState({art: e.target.value})
      }}><ChildrenZ/></Z>

      <Z sel=".research-interests .interest-market .interest-value" onChange={(e) => {
        this.setState({market: e.target.value})
      }}><ChildrenZ/></Z>


      <Z sel=".research-interests .interest-religion .interest-value" onChange={(e) => {
        this.setState({religion: e.target.value})
      }}><ChildrenZ/></Z>

      <Z sel=".research-hours .start-hour" onChange={(e) => {
        this.setState({time: e.target.value})
      }}>
      {
        this.getHourArray().map((hour) => {
          return <option value={hour}>{hour}</option>
        })
      }
      </Z>
      {/* <Z sel=".research-pos .lat-input" onChange={(e) => {
        this.setState({lat: e.target.value})
      }}><ChildrenZ/></Z>
      <Z sel=".research-pos .long-input" onChange={(e) => {
        this.setState({long: e.target.value})
      }}><ChildrenZ/></Z> */}

      <Z sel=".research-submit .ok-button" onClick={(e) => {
        e.preventDefault()

        console.log(this.state)
        this.props.callback(this.state);
      }}><ChildrenZ/></Z>

      <Z sel=".research-submit .ko-button" onClick={(e) => {
        e.preventDefault()
        this.props.callback(false);
      }}><ChildrenZ/></Z>
    </JSXZ>
  }
})