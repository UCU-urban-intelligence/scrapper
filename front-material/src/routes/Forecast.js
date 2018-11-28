import React from "react";
import SimpleTable from "../components/SimpleTable";
import Typography from "@material-ui/core/Typography/Typography";
import {withStyles} from "@material-ui/core";
import Divider from "@material-ui/core/Divider/Divider";
import Table from "@material-ui/core/Table/Table";
import TableHead from "@material-ui/core/TableHead/TableHead";
import TableRow from "@material-ui/core/TableRow/TableRow";
import TableCell from "@material-ui/core/TableCell/TableCell";
import TableBody from "@material-ui/core/TableBody/TableBody";
import Paper from "@material-ui/core/Paper/Paper";

const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar,
  tableContainer: {
    minHeight: 500,
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
        <Divider />
        <Typography variant="h5" gutterBottom component="h2">
          Your characteristics:
        </Typography>
        <Divider />
        <div className={classes.tableContainer}>
          <SimpleTable data={{
              air_quality: 66,
              area: 2534.762294883396,
              closest_shop: 99,
              cloud_cover: 0.73,
              efficiency: 6.197150269186258,
              flat_roof: 0,
              gabled_roof: 0,
              height: 12,
              humidity: 0.7,
              id: "100",
              inappropriate_type: 0,
              round_roof: 0,
              shops_amount: 15,
              temperature: 10.03}}
          />
        </div>
        <Typography variant="h5" gutterBottom component="h2">
          Predictions:
        </Typography>
        <Divider />
        <div className={classes.tableContainer}>
          <Paper className={classes.root}>
            <Table className={classes.table}>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Value</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                <TableRow key={0}>
                  <TableCell component="th" scope="row">Tomatoes:</TableCell>
                  <TableCell>15%</TableCell>
                </TableRow>
                <TableRow key={0}>
                  <TableCell component="th" scope="row">Peppers:</TableCell>
                  <TableCell>20%</TableCell>
                </TableRow>
                <TableRow key={0}>
                  <TableCell component="th" scope="row">Cucumbers:</TableCell>
                  <TableCell>65%</TableCell>
                </TableRow>
                <TableRow key={0}>
                  <TableCell component="th" scope="row">Lettuce:</TableCell>
                  <TableCell>2%</TableCell>
                </TableRow>
                <TableRow key={0}>
                  <TableCell component="th" scope="row">Carrots:</TableCell>
                  <TableCell>3%</TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </Paper>
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(Forecast);