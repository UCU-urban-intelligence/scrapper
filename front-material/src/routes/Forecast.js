import React from "react";
import SimpleTable from "../components/SimpleTable";
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";

const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar,
  tableContainer: {
    height: 320,
  }
});

class Forecast extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div>
        <div className={classes.appBarSpacer} />
        <Typography variant="h4" gutterBottom component="h2">
          Forecast
        </Typography>
        <div className={classes.tableContainer}>
          <SimpleTable />
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(Forecast);