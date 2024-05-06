import { createSlice, createAsyncThunk, current } from "@reduxjs/toolkit";
import { load } from "js-yaml";
import { isEmptyValue } from "../common/utils";

export const dataInitialize = createAsyncThunk(
  "data/dataInitialize",
  async () => {
    const result = await import.meta.glob("../posts/*.md", {
      eager: true,
      as: "raw",
    });

    return result;
  }
);

export const getRealEstate = createAsyncThunk(
  "data/getRealEstate",
  async () => {
    const jsonContext = await import.meta.glob("../data/*.json");
    const result = await Promise.all(
      Object.entries(jsonContext).map(async ([path, resolver]) => {
        const json = await resolver();
        return { path, content: json.default };
      })
    );

    return result;
  }
);

const initialState = {
  data: [],
  list: [],
  category: {},
  realEstateData: [],
};

export const dataSlice = createSlice({
  name: "data",
  initialState,
  reducers: {
    getList: (state, action) => {
      const id = action?.payload?.replaceAll(" ", "-")?.toLowerCase();
      const c = current(state.category);
      let list = [];
      if (isEmptyValue(id)) {
        Object.entries(c).forEach((item) => {
          list = [...list, ...item[1]];
        });
      } else {
        list = Object.entries(c).find(
          (e) => e?.[0].replaceAll(" ", "-")?.toLowerCase() === id
        )?.[1];
      }

      // 날짜 내림차순
      // if (list.length > 1) {
      //   list?.sort((a, b) => {
      //     const dateA = a?.header?.date;
      //     const dateB = b?.header?.date;

      //     return dateB - dateA;
      //   });
      // }

      state.list = list;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(dataInitialize.fulfilled, (state, action) => {
        const rawData = action.payload;

        const contents = Object.entries(rawData).map((file) => {
          return file[1];
        });

        const frontMatterRegex = /^---\n([\s\S]*?)\n---/;
        const list = {};
        contents.forEach((item) => {
          const match = item.match(frontMatterRegex);
          const header = load(match[1]);
          const { category, title } = header;
          const pageId = title.replaceAll(" ", "-")?.toLowerCase();
          const content = {
            categoryId: category?.replaceAll(" ", "-")?.toLowerCase(),
            pageId: pageId,
            header: { ...header, id: pageId },
            content: item.split(match[0])[1],
          };

          if (list?.[category]?.length > 0) {
            list[category] = [...list[category], content];
          } else {
            list[category] = [content];
          }
        });

        state.data = contents;
        state.category = list;
      })
      .addCase(getRealEstate.fulfilled, (state, action) => {
        const data = action.payload;
        state.realEstateData = data;
      });
  },
});

export const { getList } = dataSlice.actions;
export default dataSlice.reducer;
