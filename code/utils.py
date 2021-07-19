import os
import numpy as np
import rwaterio


def draw_pseudocolor_raster(
    image,
    colors,
    meta,
    meta_name,
    out_raster_path,
    start_date,
    end_date,
    request_id,
    annotated=False,
):
    labels = []
    result_3c = image.reshape(1, image.shape[-2], image.shape[-1])
    mask = np.zeros((image.shape[-2], image.shape[-1], 3)).astype(np.uint8)

    for ix, key in enumerate(colors.keys()):

        mask[result_3c[0] == ix] = colors[key]
        class_area = (np.where(mask[result_3c[0] == ix], 1, 0).sum()) / (3 * 10 ** 4)

        labels.append(
            {
                "color": ",".join(str(colors[key]).split(",")),
                "name": key,
                "area": round(class_area, 3),
            }
        )

    meta["height"] = ndvi_image.shape[-2]
    meta["width"] = ndvi_image.shape[-1]
    meta["transform"] = tfs
    meta["dtype"] = rasterio.uint8

    meta.update(count=3, nodata=0, compress="lzw", photometric="RGB")

    labels = json.dumps(labels)

    if not os.path.exists(out_raster_path):
        with rasterio.open(out_raster_path, "w", **meta) as dst:
            if annotated:
                dst.update_tags(
                    start_date=start_date,
                    end_date=end_date,
                    request_id=str(request_id),
                    labels=labels,
                    name=meta_name,
                )
            else:
                dst.update_tags(
                    start_date=start_date,
                    end_date=end_date,
                    request_id=str(request_id),
                    name=meta_name,
                )

            for i in range(mask.shape[-1]):
                dst.write(mask[:, :, i].astype(np.uint8), indexes=i + 1)
