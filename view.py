def image_page(images=[]):
  output = []
  for image in images:
    if image['layout'] == 'transform' or image['layout'] == 'modal_dfc':
      output.append(image['card_faces'][0]['image_uris']['png'])
    else:
      output.append(image['image_uris']['png'])
  return output