import React from "react";
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";

const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar
});

class Settings extends React.Component {
  render() {
    const { classes } = this.props;
    return (
      <div>
        <div className={classes.appBarSpacer} />
        <Typography variant="h4" gutterBottom component="h2">
          Settings
        </Typography>
      </div>
    )
  }
}

export default withStyles(styles)(Settings);