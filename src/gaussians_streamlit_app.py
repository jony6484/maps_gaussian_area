import streamlit as st
from streamlit import cli as stcli
import matplotlib.pyplot as plt
from gauss_envelope import GaussEnvelope
from file_handler import point_file_reader
import sys


def main():
    # Session states:
    if 'sigma' not in st.session_state:
        st.session_state['sigma'] = None
    if 'thresh' not in st.session_state:
        st.session_state['thresh'] = None

    # Header:
    header_cont = st.container()

    # File input area:
    file_cont = st.container()
    # Hyper params:
    params_cont = st.container()

    # Plot:
    plot_cont = st.container()



    with header_cont:
        st.title('Gaussian Contours')

    with file_cont:
        st.text("here will be the file input zone")
        uploaded_file = st.file_uploader("format is a two column csv ONLY", type='csv')
        if uploaded_file is not None:
            lines = uploaded_file.getvalue().decode("utf-8").split('\n')
            points_list, points_arr = point_file_reader(lines)
            st.text("file is in!!!")
            gauss_env = GaussEnvelope(points_arr)
            polygon = gauss_env.mk_convex_polygon(return_value=True)
            ############################
        else:
            st.stop()
    with params_cont:
        sigma_col, thresh_col = st.columns(2)
        sigma = sigma_col.slider(
            'sigma:', min_value=0.001, max_value=0.05, value=0.012, step=0.001, format="%f")
        thresh = thresh_col.slider('thresh:', min_value=0.001, max_value=0.9, value=0.1, step=0.001)
        gauss_env.calc_gauss_grid(sigma=sigma)
        gauss_env.find_contours(thresh=thresh)

    with plot_cont:
        st.text("here will be the plot of the contours")
        fig, ax = plt.subplots()
        ax.contour(gauss_env.xx, gauss_env.yy, gauss_env.gauss_grid, 15)
        for contour in gauss_env.contour_point_lst:
            ax.plot(contour[:, 0], contour[:, 1], 'r--')
        ax.plot(gauss_env.points[:, 0], gauss_env.points[:, 1], 'k.')
        ax.set_aspect('equal')
        ax.grid()
        st.pyplot(fig)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())