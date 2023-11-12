import { KeyboardArrowRight } from "@mui/icons-material";
import { useLocation } from "react-router-dom";
import { useEffect } from "react";
import { Breadcrumbs, Typography } from "@mui/material";

const Breadcrum = () => {
  const location = useLocation();

  useEffect(() => {
    console.log("location->", location);
  }, [location]);

  return (
    <Breadcrumbs separator={<KeyboardArrowRight />} aria-label="breadcrumbs">
      <Typography>About</Typography>
    </Breadcrumbs>
  );
};

export default Breadcrum;
