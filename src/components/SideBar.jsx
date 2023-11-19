import { useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Avatar,
  Box,
  Drawer,
  IconButton,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  Typography,
} from "@mui/material";

import HomeIcon from "@mui/icons-material/Home";
import Brightness4Icon from "@mui/icons-material/Brightness4";
import Brightness7Icon from "@mui/icons-material/Brightness7";
import EmailIcon from "@mui/icons-material/Email";
import MenuIcon from "@mui/icons-material/Menu";
import DataArrayIcon from "@mui/icons-material/DataArray";
import DataObjectIcon from "@mui/icons-material/DataObject";
import CodeIcon from "@mui/icons-material/Code";
import BuildIcon from "@mui/icons-material/Build";
// import NewspaperIcon from "@mui/icons-material/Newspaper";
// import ApiIcon from "@mui/icons-material/Api";
// import BoltIcon from "@mui/icons-material/Bolt";
// import JavascriptIcon from "@mui/icons-material/Javascript";
import img from "../assets/images/profile.png";

const ICONS = [
  <DataArrayIcon key={0} />,
  <DataObjectIcon key={1} />,
  <CodeIcon key={2} />,
  <BuildIcon key={3} />,
];

const SideBar = ({ mode, modeToggle, dataList }) => {
  const navigate = useNavigate();
  const [drawerToggle, setDrawerToggle] = useState(false);

  const drawer = () => {
    return (
      <>
        <Box sx={{ textAlign: "center", mt: 2, mb: 5 }}>
          <Avatar
            src={img}
            sx={{ width: 150, height: 150, margin: "0px auto" }}
          />
          <Typography
            variant="h5"
            sx={{ mt: 3, fontFamily: "cursive, Poppins, sans-serif" }}
          >
            Hello Sushi
          </Typography>
          <Typography
            mt={1}
            sx={{
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: 12,
            }}
            gap={1}
          >
            <EmailIcon />
            nyimpe52@gmail.com
          </Typography>
        </Box>
        <Box sx={{ height: "90%" }}>
          <List>
            <ListItem>
              <ListItemButton onClick={() => navigate("/")}>
                <ListItemIcon>
                  <HomeIcon />
                </ListItemIcon>
                HOME
              </ListItemButton>
            </ListItem>
            {Object.keys(dataList).length > 0 ? (
              <>
                {Object.keys(dataList).map((e, i) => {
                  return (
                    <ListItem key={e}>
                      <ListItemButton component="a" href="#actionable">
                        <ListItemIcon>{ICONS[i]}</ListItemIcon>
                        <Typography>{e}</Typography>
                      </ListItemButton>
                    </ListItem>
                  );
                })}
              </>
            ) : null}
          </List>
        </Box>
        <Box sx={{ textAlign: "center", mb: 3 }}>
          <IconButton onClick={modeToggle} color="inherit">
            {mode === "dark" ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Box>
      </>
    );
  };

  return (
    <>
      <Box sx={{ m: 1 }}>
        <IconButton onClick={() => setDrawerToggle(true)}>
          <MenuIcon />
        </IconButton>
      </Box>
      <Drawer
        sx={{
          width: 250,
          flexShrink: 0,
          "& .MuiDrawer-paper": {
            width: 250,
            boxSizing: "border-box",
            justifyContent: "space-between",
          },
          display: { lg: "block", md: "block", sm: "none", xs: "none" },
        }}
        variant="permanent"
        ModalProps={{ keepMounted: true }}
        anchor="left"
        open={drawerToggle}
        onClose={() => setDrawerToggle(false)}
      >
        {drawer()}
      </Drawer>
      <Drawer
        variant="temporary"
        open={drawerToggle}
        onClose={() => setDrawerToggle(false)}
        ModalProps={{ keepMounted: true }}
        sx={{
          "& .MuiDrawer-paper": {
            width: 250,
            boxSizing: "border-box",
            justifyContent: "space-between",
          },
          display: { lg: "none", md: "none", sm: "block", xs: "block" },
        }}
      >
        {drawer()}
      </Drawer>
    </>
  );
};

export default SideBar;