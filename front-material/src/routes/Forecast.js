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
import FormControl from "@material-ui/core/FormControl/FormControl";
import InputLabel from "@material-ui/core/InputLabel/InputLabel";
import MenuItem from "@material-ui/core/MenuItem/MenuItem";
import Select from "@material-ui/core/Select/Select";

const styles = theme => ({
  appBarSpacer: theme.mixins.toolbar,
  tableContainer: {
    minHeight: 500,
  }
});

class Forecast extends React.Component {
  constructor(...args) {
    super(...args);
    this.state = {
      open: false
    }
  }

  render() {
    const { classes } = this.props;
    return (
      <div>
        <div className={classes.appBarSpacer} />
        <div style={{display: "flex", alignItems: "center"}}>
          <Typography variant="h4" gutterBottom component="h2">
            Forecast
          </Typography>
          <FormControl className={classes.formControl} style={{marginLeft: "570px", width: "400px"}}>
            <InputLabel htmlFor="demo-controlled-open-select">530 Adelaide St W #108, Toronto, ON M5V 1T5</InputLabel>
            <Select
              open={this.state.open}
              onClose={this.handleClose}
              onOpen={this.handleOpen}
              value={this.state.age}
              onChange={this.handleChange}
              inputProps={{
                name: 'age',
                id: 'demo-controlled-open-select',
              }}
            >
              <MenuItem value="">
                <em>None</em>
              </MenuItem>
              <MenuItem value={10}>Ten</MenuItem>
              <MenuItem value={20}>Twenty</MenuItem>
              <MenuItem value={30}>Thirty</MenuItem>
            </Select>
          </FormControl>
        </div>
        <Divider />
        <div style={{display: "flex"}}>
          <div>
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
          </div>
          <div>
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
                    <TableRow>
                      <TableCell component="th" scope="row">Carrots:</TableCell>
                      <TableCell>25%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell component="th" scope="row">Tomatoes:</TableCell>
                      <TableCell>15%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell component="th" scope="row">Peppers:</TableCell>
                      <TableCell>12%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell component="th" scope="row">Cucumbers:</TableCell>
                      <TableCell>10%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell component="th" scope="row">Lettuce:</TableCell>
                      <TableCell>7%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell component="th" scope="row">Potato:</TableCell>
                      <TableCell>6%</TableCell>
                    </TableRow>
                    <TableRow>
                      <TableCell component="th" scope="row">...</TableCell>
                    </TableRow>
                  </TableBody>
                </Table>
              </Paper>
            </div>
          </div>
        </div>
      </div>
    )
  }
}

export default withStyles(styles)(Forecast);