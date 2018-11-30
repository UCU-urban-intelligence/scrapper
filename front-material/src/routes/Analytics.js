import Typography from "@material-ui/core/Typography/Typography";
import SimpleLineChart from "../components/SimpleLineChart";
import SimplePieChart from "../components/SimplePieChart";
import SimpleBarChart from "../components/SimpleBarChart";
import React from "react";
import {withStyles} from "@material-ui/core";

const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar,
  chartContainer: {
    marginLeft: -22,
    display: 'flex',
    justifyContent: 'center'
  },
  tableContainer: {
    height: 320,
  }
});


class Analytics extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div>
        <div className={classes.appBarSpacer} />
        <Typography variant="h4" gutterBottom component="h2">
          Analytics
        </Typography>
        <div style={{display: 'flex'}}>
          <SimpleLineChart style={{width: '50%'}} />
          <SimpleBarChart style={{width: '50%'}} />
        </div>
        <Typography component="div" className={classes.chartContainer}>
          <SimplePieChart />
        </Typography>
      </div>
    )
  }
}

export default withStyles(styles)(Analytics);