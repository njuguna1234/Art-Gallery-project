import React from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';

function ArtworkForm() {
  const formik = useFormik({
    initialValues: {
      title: '',
      description: '',
      price: '',
    },
    validationSchema: Yup.object({
      title: Yup.string().required('Title is required'),
      description: Yup.string().required('Description is required'),
      price: Yup.number().positive('Price must be a positive number').required('Price is required'),
    }),
    onSubmit: (values) => {
      fetch('/api/artworks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(values),
      })
        .then((response) => response.json())
        .then((data) => console.log(data))
        .catch((error) => console.error('Error:', error));
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <h1>Add Artwork</h1>
      <label>Title</label>
      <input type="text" name="title" {...formik.getFieldProps('title')} />
      {formik.touched.title && formik.errors.title ? <div>{formik.errors.title}</div> : null}

      <label>Description</label>
      <textarea name="description" {...formik.getFieldProps('description')}></textarea>
      {formik.touched.description && formik.errors.description ? <div>{formik.errors.description}</div> : null}

      <label>Price</label>
      <input type="number" name="price" {...formik.getFieldProps('price')} />
      {formik.touched.price && formik.errors.price ? <div>{formik.errors.price}</div> : null}

      <button type="submit">Add Artwork</button>
    </form>
  );
}

export default ArtworkForm;