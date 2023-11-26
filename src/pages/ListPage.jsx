import { useEffect } from "react";
import { useDispatch, useSelector } from "react-redux";
import { useParams } from "react-router-dom";
import { nanoid } from "@reduxjs/toolkit";
import dayjs from "dayjs";
import { Box, Card, CardContent, Typography } from "@mui/material";
import JavascriptIcon from "@mui/icons-material/Javascript";
import CalendarMonthOutlinedIcon from "@mui/icons-material/CalendarMonthOutlined";

import { getList } from "../features/dataSlice";
import { isEmptyValue } from "../common/utils";

const ListPage = () => {
  const param = useParams();
  const dispatch = useDispatch();
  const { category, list } = useSelector((state) => state.data);

  useEffect(() => {
    if (isEmptyValue(category)) {
      return;
    }
    dispatch(getList(param.category));
  }, [category, param, dispatch]);

  return (
    <Box sx={{ my: 3 }}>
      {!isEmptyValue(list)
        ? list.map((item) => {
            return (
              <Card key={nanoid()} sx={{ my: 2 }} variant="outlined">
                <CardContent>
                  <Typography fontSize={18} fontWeight={"bold"} gutterBottom>
                    {item.header.title}
                  </Typography>
                  <Typography
                    sx={{
                      my: 1,
                      maxHeight: 50,
                      overflow: "hidden",
                      wordBreak: "break-word",
                    }}
                    color="text.secondary"
                  >
                    {item.content}
                  </Typography>
                  <Box
                    sx={{
                      display: "flex",
                      gap: 1,
                      mt: 2,
                      alignItems: "center",
                    }}
                  >
                    <CalendarMonthOutlinedIcon />
                    <Typography
                      variant="body2"
                      color="text.secondary"
                      sx={{ mr: 5 }}
                    >
                      {dayjs(item.header.date).format("YYYY.MM.DD.")}
                    </Typography>

                    <JavascriptIcon />
                    <Typography variant="body2" color="text.secondary">
                      {item.header.category}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            );
          })
        : null}
    </Box>
  );
};

export default ListPage;
