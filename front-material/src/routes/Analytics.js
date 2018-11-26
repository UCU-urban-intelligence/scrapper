import Typography from "@material-ui/core/Typography/Typography";
import SimpleLineChart from "../components/SimpleLineChart";
import React from "react";
import {withStyles} from "@material-ui/core";
import SimplePieChart from "../components/SimplePieChart";

const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar,
  chartContainer: {
    marginLeft: -22,
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
        <Typography component="div" className={classes.chartContainer}>
          <SimpleLineChart />
        </Typography>
        <Typography component="div" className={classes.chartContainer}>
          <SimplePieChart />
        </Typography>
      </div>
    )
  }
}

export default withStyles(styles)(Analytics);