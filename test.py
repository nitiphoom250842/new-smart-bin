# from core.log import LogSystems


# # log_instance = LogSystems(data=None, type_log='error')
# # data = log_instance.read_csv_file()
# # print(data)

# push_log_instance = LogSystems(data=[[1,2,3],[4,5,6]], type_log='error')
# data = push_log_instance.write_csv_file()
# print(data)

# import staticmaps

# context = staticmaps.Context()
# context.set_tile_provider(staticmaps.tile_provider_StamenToner)

# frankfurt = staticmaps.create_latlng(50.110644, 8.682092)
# newyork = staticmaps.create_latlng(40.712728, -74.006015)

# context.add_object(staticmaps.Line([frankfurt, newyork], color=staticmaps.BLUE, width=4))
# context.add_object(staticmaps.Marker(frankfurt, color=staticmaps.GREEN, size=12))
# context.add_object(staticmaps.Marker(newyork, color=staticmaps.RED, size=12))

# # # render non-anti-aliased png
# # image = context.render_pillow(800, 500)
# # image.save("frankfurt_newyork.pillow.png")

# # # render anti-aliased png (this only works if pycairo is installed)
# # image = context.render_cairo(800, 500)
# # image.write_to_png("frankfurt_newyork.cairo.png")

# # render svg
# svg_image = context.render_svg(800, 500)
# with open("frankfurt_newyork.svg", "w", encoding="utf-8") as f:
#     svg_image.write(f, pretty=True)

import staticmaps

context = staticmaps.Context()
context.set_tile_provider(staticmaps.tile_provider_StamenToner)

center1 = staticmaps.create_latlng(66, 0)
center2 = staticmaps.create_latlng(0, 0)

context.add_object(
    staticmaps.Circle(
        center1, 2000, fill_color=staticmaps.TRANSPARENT, color=staticmaps.RED, width=2
    )
)
context.add_object(
    staticmaps.Circle(
        center2,
        2000,
        fill_color=staticmaps.TRANSPARENT,
        color=staticmaps.GREEN,
        width=2,
    )
)
context.add_object(staticmaps.Marker(center1, color=staticmaps.RED))
context.add_object(staticmaps.Marker(center2, color=staticmaps.GREEN))

# # render non-anti-aliased png
# image = context.render_pillow(800, 500)
# image.save("geodesic_circles.pillow.png")

# # render anti-aliased png (this only works if pycairo is installed)
# image = context.render_cairo(800, 600)
# image.write_to_png("geodesic_circles.cairo.png")

# # render svg
svg_image = context.render_svg(800, 500)
with open("frankfurt_newyork.svg", "w", encoding="utf-8") as f:
    svg_image.write(f, pretty=True)
